# Copyright (C) 2026 Fernando de Paula Zamboni
# SPDX-License-Identifier: GPL-2.0-or-later
"""ChatGPT Companion: foreground-only accessibility monitoring; no network access."""
import time
import addonHandler
import api
import config
import controlTypes
import globalPluginHandler
import globalVars
import gui
from gui import guiHelper
from gui.settingsDialogs import SettingsPanel, NVDASettingsDialog
from scriptHandler import script
import textInfos
import ui
import wx
from .engine import Tracker, allowed_url, parse_tokens

addonHandler.initTranslation()
SECTION = 'fzChatGPTCompanion'
SPEC = {
    'enabled': 'boolean(default=True)',
    'readSent': 'boolean(default=True)',
    'confirmSent': 'boolean(default=True)',
    'readAnswers': 'boolean(default=True)',
    'readStatus': 'boolean(default=True)',
    'ignoreInterface': 'boolean(default=True)',
    'mode': 'option(complete, progressive, default=complete)',
    'settleSeconds': 'integer(default=2, min=1, max=10)',
    'fallbackSeconds': 'integer(default=3, min=0, max=60)',
}


class CompanionSettings(SettingsPanel):
    title = _('ChatGPT Companion')

    def makeSettings(self, settingsSizer):
        helper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
        self.checks = {}
        for key, label in (
            ('enabled', _('Enable automatic reading')),
            ('readSent', _('Read sent messages')),
            ('confirmSent', _('Confirm sending when reading sent messages is disabled')),
            ('readAnswers', _('Read answers')),
            ('readStatus', _('Read progress updates')),
            ('ignoreInterface', _('Ignore interface notices and footer text')),
        ):
            widget = helper.addItem(wx.CheckBox(self, label=label))
            widget.SetValue(config.conf[SECTION][key])
            self.checks[key] = widget
        self.mode = helper.addLabeledControl(_('Answer reading mode'), wx.Choice,
            choices=[_('Complete answer'), _('New paragraphs (experimental)')])
        self.mode.SetSelection(0 if config.conf[SECTION]['mode'] == 'complete' else 1)
        self.delay = helper.addLabeledControl(_('Wait after completion (seconds)'), wx.SpinCtrl, min=1, max=10)
        self.delay.SetValue(config.conf[SECTION]['settleSeconds'])
        self.fallback = helper.addLabeledControl(_('Fallback after silence (seconds; 0 disables)'), wx.SpinCtrl, min=0, max=60)
        self.fallback.SetValue(config.conf[SECTION]['fallbackSeconds'])
        helper.addItem(wx.StaticText(self, label=_(
            'Only the active ChatGPT conversation is monitored. The silence fallback can mistake a pause for completion.')))

    def onSave(self):
        for key, widget in self.checks.items():
            config.conf[SECTION][key] = widget.GetValue()
        config.conf[SECTION]['mode'] = 'complete' if self.mode.GetSelection() == 0 else 'progressive'
        config.conf[SECTION]['settleSeconds'] = self.delay.GetValue()
        config.conf[SECTION]['fallbackSeconds'] = self.fallback.GetValue()


def announcement_text(kind, text, settings):
    """The single output gate, also used by tests of the actual speech policy."""
    if kind == 'user':
        if settings['readSent']:
            return _('You said: {text}').format(text=text)
        if settings['confirmSent']:
            return _('Message sent.')
    elif kind == 'answer' and settings['readAnswers']:
        return _('ChatGPT: {text}').format(text=text)
    elif kind == 'status' and settings['readStatus']:
        return _('Progress: {text}').format(text=text)
    return None


def role_name(role):
    return getattr(role, 'name', '')


def field_tokens(fields):
    """Reduce NVDA text fields without accessing DOM/private browser protocols."""
    tokens, stack = [], []
    capture = None
    for item in fields:
        if isinstance(item, str):
            if capture is not None:
                capture['text'].append(item)
            else:
                tokens.append(('text', item))
            continue
        command = getattr(item, 'command', '')
        field = getattr(item, 'field', {}) or {}
        if command == 'controlStart':
            role = role_name(field.get('role'))
            stack.append(role)
            if capture is None and role in {'HEADING', 'BUTTON', 'TOGGLEBUTTON', 'EDITABLETEXT', 'STATUSBAR'}:
                capture = {'kind': {'HEADING': 'heading', 'BUTTON': 'button', 'TOGGLEBUTTON': 'button',
                    'EDITABLETEXT': 'edit', 'STATUSBAR': 'status'}[role],
                    'depth': len(stack), 'name': field.get('name', ''), 'text': []}
            elif capture is None and role in {'PARAGRAPH', 'SECTION', 'ARTICLE', 'LISTITEM'}:
                tokens.append(('text', '\n'))
        elif command == 'controlEnd':
            if capture is not None and capture['depth'] == len(stack):
                content = ''.join(capture['text']).strip() or capture['name'] or ''
                tokens.append((capture['kind'], content))
                capture = None
            if stack:
                role = stack.pop()
                if capture is None and role in {'PARAGRAPH', 'SECTION', 'ARTICLE', 'LISTITEM'}:
                    tokens.append(('text', '\n'))
    return tokens


def document_context():
    focus = api.getFocusObject()
    if not focus:
        return None
    app = focus.appModule.appName.casefold()
    if app not in {'chrome', 'msedge', 'firefox', 'brave', 'chatgpt'}:
        return None
    # NVDA's browse-mode buffer exposes structured text even while the composer has focus.
    node = focus
    for _depth in range(20):
        interceptor = getattr(node, 'treeInterceptor', None)
        if interceptor and getattr(interceptor, 'isReady', True):
            root = getattr(interceptor, 'rootNVDAObject', node)
            url = getattr(interceptor, 'documentURL', None) or getattr(root, 'value', '') or ''
            if allowed_url(url) or (app == 'chatgpt' and root.role == controlTypes.Role.DOCUMENT):
                return interceptor, root, url, app
        if node.role == controlTypes.Role.DOCUMENT:
            url = getattr(node, 'value', '') or ''
            if allowed_url(url) or app == 'chatgpt':
                return node, node, url, app
        node = node.parent
        if node is None:
            break
    return None


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _('ChatGPT Companion')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer = None
        self.root = None
        self.url = None
        self.tracker = Tracker()
        self.diagnostic = _('No supported conversation detected.')
        self.active = False
        if globalVars.appArgs.secure:
            return
        config.conf.spec[SECTION] = SPEC
        if CompanionSettings not in NVDASettingsDialog.categoryClasses:
            NVDASettingsDialog.categoryClasses.append(CompanionSettings)
        self.timer = wx.CallLater(1200, self._tick)

    def terminate(self):
        self.active = False
        if self.timer:
            self.timer.Stop()
            self.timer = None
        if CompanionSettings in NVDASettingsDialog.categoryClasses:
            NVDASettingsDialog.categoryClasses.remove(CompanionSettings)
        self.tracker = Tracker()
        super().terminate()

    def _reset(self):
        self.root = None
        self.url = None
        self.active = False
        self.tracker = Tracker()

    def _tick(self):
        try:
            if not config.conf[SECTION]['enabled']:
                self._reset()
                self.diagnostic = _('Automatic reading is disabled.')
                return
            context = document_context()
            if not context:
                self._reset()
                self.diagnostic = _('No supported conversation detected.')
                return
            reader, root, url, app = context
            # Creating a new conversation may change / to /c/<id> in the same document.
            new_chat_url = (self.url and self.url.rstrip('/') in {'https://chatgpt.com', 'https://chat.openai.com'}
                            and '/c/' in url)
            if root != self.root or (url != self.url and not new_chat_url):
                self.tracker = Tracker()
            self.root, self.url = root, url
            info = reader.makeTextInfo(textInfos.POSITION_ALL)
            # Do not scan giant histories in the screen reader's UI thread.
            if len(info.text) > 250000:
                self.diagnostic = _('Conversation too long. Open a shorter conversation for automatic reading.')
                self.tracker = Tracker()
                self.active = False
                return
            snapshot = parse_tokens(field_tokens(info.getTextWithFields()),
                ignore_interface=config.conf[SECTION]['ignoreInterface'])
            self.active = True
            self.diagnostic = _('Messages: {count}. Generation control: {state}.').format(
                count=len(snapshot.messages), state=(_('busy') if snapshot.busy is True else
                _('idle') if snapshot.busy is False else _('not detected')))
            settings = config.conf[SECTION]
            events = self.tracker.update(snapshot, time.monotonic(), settings['mode'],
                settings['settleSeconds'], settings['fallbackSeconds'])
            for kind, text in events:
                announcement = announcement_text(kind, text, settings)
                if announcement:
                    ui.message(announcement)
        except Exception:
            # Deliberately never log conversation text, URLs or exception messages.
            self._reset()
            self.diagnostic = _('Accessible text unavailable. Try browse mode or another supported browser.')
        finally:
            if self.timer is not None:
                self.timer = wx.CallLater(1200, self._tick)

    @script(description=_('Toggle automatic ChatGPT reading'), gesture='kb:NVDA+control+shift+g')
    def script_toggle(self, gesture):
        if globalVars.appArgs.secure:
            return
        settings = config.conf[SECTION]
        settings['enabled'] = not settings['enabled']
        self._reset()
        ui.message(_('Automatic reading enabled.') if settings['enabled'] else _('Automatic reading disabled.'))

    @script(description=_('Read the latest available ChatGPT answer'), gesture='kb:NVDA+control+shift+r')
    def script_repeat(self, gesture):
        if globalVars.appArgs.secure:
            return
        self._tick_manual_refresh()
        ui.message(self.tracker.last_answer if self.active and self.tracker.last_answer else _('No answer available.'))

    def _tick_manual_refresh(self):
        # Manual commands work even when automatic reading is disabled.
        try:
            context = document_context()
            if context:
                reader, root, url, app = context
                info = reader.makeTextInfo(textInfos.POSITION_ALL)
                if len(info.text) <= 250000:
                    snapshot = parse_tokens(field_tokens(info.getTextWithFields()),
                ignore_interface=config.conf[SECTION]['ignoreInterface'])
                    if root != self.root or url != self.url:
                        self.tracker = Tracker()
                    self.root, self.url = root, url
                    answers = [m.text for m in snapshot.messages if m.role == 'assistant']
                    self.tracker.last_answer = answers[-1] if answers else ''
                    self.tracker.last_status = snapshot.status
                    self.active = True
                    return
        except Exception:
            pass
        self._reset()

    @script(description=_('Read the latest progress update'), gesture='kb:NVDA+control+shift+p')
    def script_progress(self, gesture):
        if globalVars.appArgs.secure:
            return
        self._tick_manual_refresh()
        ui.message(self.tracker.last_status if self.active and self.tracker.last_status else _('No progress update available.'))

    @script(description=_('Report ChatGPT accessibility diagnostics'), gesture='kb:NVDA+control+shift+d')
    def script_diagnostic(self, gesture):
        if globalVars.appArgs.secure:
            return
        ui.message(self.diagnostic)
