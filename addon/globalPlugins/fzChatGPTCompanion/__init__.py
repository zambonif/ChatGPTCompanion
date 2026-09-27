# Copyright (C) 2026 Fernando de Paula Zamboni
# SPDX-License-Identifier: GPL-2.0-or-later
"""ChatGPT Companion: foreground-only accessibility monitoring; no network access."""
import time
from collections import OrderedDict
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
from .reading import read_snapshot

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
                    'depth': len(stack), 'name': field.get('name', ''), 'text': [],
                    'identity': str(field.get('uniqueID') or field.get('runtimeID') or '')}
            elif capture is None and role in {'PARAGRAPH', 'SECTION', 'ARTICLE', 'LISTITEM'}:
                tokens.append(('text', '\n'))
        elif command == 'controlEnd':
            if capture is not None and capture['depth'] == len(stack):
                content = ''.join(capture['text']).strip() or capture['name'] or ''
                if capture['kind'] == 'heading':
                    tokens.append((capture['kind'], content, capture['identity']))
                else:
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
        self.sessions = OrderedDict()
        self.session_key = None
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
        self.sessions.clear()
        super().terminate()

    def _reset(self):
        self.root = None
        self.url = None
        self.active = False
        self.tracker = Tracker()
        self.session_key = None
        self.sessions.clear()

    def _select_context(self, context):
        reader, root, url, app = context
        # Separate different windows even if they show the same conversation URL.
        key = (app, getattr(root, 'processID', None), getattr(root, 'windowHandle', None), url)
        new_chat_url = (self.url and self.url.rstrip('/') in {'https://chatgpt.com', 'https://chat.openai.com'}
                        and '/c/' in url and root == self.root)
        if key not in self.sessions:
            if new_chat_url and self.session_key in self.sessions:
                self.sessions[key] = self.sessions.pop(self.session_key)
            else:
                self.sessions[key] = Tracker()
        self.tracker = self.sessions[key]
        self.sessions.move_to_end(key)
        while len(self.sessions) > 8:
            self.sessions.popitem(last=False)
        self.root, self.url, self.session_key = root, url, key
        return reader

    def _snapshot(self, context):
        reader = self._select_context(context)
        return read_snapshot(reader, field_tokens, config.conf[SECTION]['ignoreInterface'])

    def _describe(self, snapshot):
        self.diagnostic = _('Messages: {count}. Generation control: {state}.').format(
            count=len(snapshot.messages), state=(_('busy') if snapshot.busy is True else
            _('idle') if snapshot.busy is False else _('not detected')))
        if not snapshot.messages:
            self.diagnostic = _('The latest conversation text is not available to NVDA. No older answer will be read.')

    def _tick(self):
        try:
            if not config.conf[SECTION]['enabled']:
                self.active = False
                self.diagnostic = _('Automatic reading is disabled.')
                return
            context = document_context()
            if not context:
                # Keep bounded per-conversation baselines while another window
                # has focus. Announcements resume only after returning to ChatGPT.
                self.active = False
                self.diagnostic = _('No supported conversation detected.')
                return
            snapshot = self._snapshot(context)
            self.active = True
            self._describe(snapshot)
            settings = config.conf[SECTION]
            events = self.tracker.update(snapshot, time.monotonic(), settings['mode'],
                settings['settleSeconds'], settings['fallbackSeconds'])
            for kind, text in events:
                announcement = announcement_text(kind, text, settings)
                if announcement:
                    ui.message(announcement)
        except Exception:
            # Do not expose cached answers on a failed current read. Keep the
            # comparison state to recover after transient accessibility errors.
            self.active = False
            self.tracker.last_answer = ''
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
        # Always read a fresh tail, even if automatic reading is disabled.
        self.active = False
        self.tracker.last_answer = ''
        context = None
        try:
            context = document_context()
            if context:
                snapshot = self._snapshot(context)
                self._describe(snapshot)
                self.tracker.last_answer = (
                    snapshot.messages[-1].text
                    if snapshot.messages and snapshot.messages[-1].role == 'assistant' else '')
                self.tracker.last_status = snapshot.status
                self.active = True
                return
        except Exception:
            self.diagnostic = _('Accessible text unavailable. Try browse mode or another supported browser.')
        self.tracker.last_answer = ''
        if not context:
            self.diagnostic = _('No supported conversation detected.')

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
        self._tick_manual_refresh()
        ui.message(self.diagnostic)
