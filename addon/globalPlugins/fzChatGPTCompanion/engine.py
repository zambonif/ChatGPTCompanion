# Copyright (C) 2026 Fernando de Paula Zamboni
# SPDX-License-Identifier: GPL-2.0-or-later
"""Pure conversation extraction and announcement state machine (no NVDA imports)."""
from dataclasses import dataclass
import re
from hashlib import sha256
from urllib.parse import urlsplit

USER_HEADINGS = {'you said', 'você disse', 'voce disse', 'tu disse', 'dijiste', 'tú dijiste', 'vous avez dit', 'hai detto'}
ASSISTANT_HEADINGS = {'chatgpt said', 'o chatgpt disse', 'chatgpt disse', 'chatgpt dijo', 'chatgpt a dit', 'chatgpt ha detto'}
STOP = {'stop generating', 'stop streaming', 'stop response', 'parar de gerar', 'interromper geração', 'parar geração', 'parar resposta', 'detener generación', 'detener la generación', 'detener respuesta', 'arrêter la génération', 'interrompi generazione', 'interrompi la generazione'}
SEND = {'send prompt', 'send message', 'send', 'enviar mensagem', 'enviar prompt', 'enviar', 'enviar mensaje', 'envoyer le message', 'envoyer', 'invia messaggio', 'invia'}
PROGRESS = ('thinking', 'pensando', 'refletindo', 'raciocinando', 'réflexion', 'ragionamento', 'sto pensando', 'searching', 'pesquisando', 'buscando', 'recherche', 'ricerca')


# Conservative fallback when accessibility flattens the footer into response text.
# Require the complete warning + latest-response label at the document tail.
# Never globally remove words or isolated sentences from a response.
FOOTERS = (
    ('O ChatGPT pode cometer erros. Confira informações importantes.', 'Resposta mais recente'),
    ('O ChatGPT pode cometer erros. Verifique informações importantes.', 'Resposta mais recente'),
    ('ChatGPT pode cometer erros. Confira informações importantes.', 'Resposta mais recente'),
    ('ChatGPT can make mistakes. Check important info.', 'Latest response'),
    ('ChatGPT can make mistakes. Check important information.', 'Latest response'),
    ('ChatGPT puede cometer errores. Comprueba la información importante.', 'Respuesta más reciente'),
    ('ChatGPT peut faire des erreurs. Vérifiez les informations importantes.', 'Réponse la plus récente'),
    ('ChatGPT può commettere errori. Verifica le informazioni importanti.', 'Risposta più recente'),
)


def strip_interface_footer(text):
    for warning, label in FOOTERS:
        # Keep quoted examples and mid-answer references intact. Match the pair
        # only as standalone trailing lines (including wrapped whitespace).
        pattern = r'(?:^|\n)[ \t]*' + r'\s+'.join(re.escape(w) for w in warning.split())
        pattern += r'\s+' + r'\s+'.join(re.escape(w) for w in label.split()) + r'\s*$'
        text = re.sub(pattern, '', text, flags=re.IGNORECASE).rstrip()
    return text


def normalized(text):
    return ' '.join(text.replace('\u00a0', ' ').split()).casefold().rstrip(':： .…')


def allowed_url(url):
    try:
        parts = urlsplit(url)
        return parts.scheme == 'https' and parts.hostname in {'chatgpt.com', 'chat.openai.com'}
    except (ValueError, AttributeError):
        return False


@dataclass(frozen=True)
class Message:
    role: str
    text: str
    identity: str = ""


@dataclass(frozen=True)
class Snapshot:
    messages: tuple = ()
    busy: object = None  # True: stop control; False: send control; None: unknown.
    status: str = ''


def parse_tokens(tokens, ignore_interface=True):
    """Actor boundaries must be actual accessibility headings, not arbitrary text."""
    messages, body = [], []
    actor = None
    identity = ""
    stop = send = False
    status = ''
    composer = False
    def flush():
        if actor:
            text = re.sub(r'[ \t]+', ' ', ''.join(body))
            text = re.sub(r'\n{3,}', '\n\n', text).strip()
            if text:
                messages.append(Message(actor, text, identity))
    for token in tokens:
        kind, text = token[:2]
        name = normalized(text)
        # A composer/editable area can occur inside old turns. A later author
        # heading always starts a new turn, including after such an edit field.
        if kind == 'heading' and name in USER_HEADINGS | ASSISTANT_HEADINGS:
            flush()
            actor = 'user' if name in USER_HEADINGS else 'assistant'
            identity = token[2] if len(token) > 2 else ''
            body = []
            composer = False
            continue
        if kind == 'button':
            stop = stop or name in STOP
            send = send or name in SEND
            if any(name.startswith(p) for p in PROGRESS):
                status = text.strip()
            continue
        if kind == 'edit':
            composer = actor is not None
            continue
        if kind == 'status':
            if text.strip():
                status = text.strip()
            continue
        if composer:
            continue
        if kind == 'heading' and any(name.startswith(p) for p in PROGRESS):
            status = text.strip()
        elif actor:
            body.append(('\n' + text + '\n') if kind == 'heading' else text)
    flush()
    if ignore_interface and actor == 'assistant' and messages and messages[-1].role == 'assistant':
        cleaned = strip_interface_footer(messages[-1].text)
        if cleaned:
            messages[-1] = Message('assistant', cleaned, messages[-1].identity)
        else:
            messages.pop()
    return Snapshot(tuple(messages), True if stop else False if send else None, status)


class Tracker:
    """Keep only one foreground conversation; baseline prevents reading old history."""
    def __init__(self):
        self.previous = None
        self.seen_user_count = 0
        self.fallback_turn = 0
        self.seen_user_ids = set()
        self.pending = None
        self.changed_at = 0.0
        self.last_status = ''
        self.status_at = -100.0
        self.last_answer = ''
        self.last_announced = None
        self.completed_answers = set()
        self.offset = 0

    def update(self, snapshot, now, mode='complete', delay=2, fallback=0):
        events = []
        old = self.previous
        # Empty transient accessibility snapshots are not a new baseline.
        # Clear manual output, but retain the previous comparison for recovery.
        if old is not None and old.messages and not snapshot.messages:
            self.last_answer = ''
            return events
        self.previous = snapshot
        answers = [(i, m.text) for i, m in enumerate(snapshot.messages) if m.role == 'assistant']
        latest = answers[-1] if answers else None

        # Once another user turn exists, the preceding answer is historical.
        # Its disappearing footer or reflow must not queue it as a new answer.
        last_user = max((i for i, m in enumerate(snapshot.messages) if m.role == 'user'), default=-1)
        if latest and latest[0] < last_user:
            latest = None
        self.last_answer = latest[1] if latest else ''
        def answer_key(entry):
            index, text = entry
            turn = sum(m.role == 'user' for m in snapshot.messages[:index])
            identity = snapshot.messages[index].identity
            digest = sha256(' '.join(text.split()).encode('utf-8')).hexdigest()
            return (identity or ('turn', self.fallback_turn, turn), digest)
        users = [m for m in snapshot.messages if m.role == 'user']
        if old is None:
            self.seen_user_count = len(users)
            self.seen_user_ids.update(m.identity for m in users if m.identity)
            self.last_status = snapshot.status
            self.completed_answers.update(answer_key(entry) for entry in answers)
            return events
        # A shrinking history is likely navigation/virtualisation: establish a new baseline.
        has_ids = bool(users and users[-1].identity)
        if not has_ids and len(snapshot.messages) < len(old.messages):
            self.pending = None
            self.offset = 0
            self.seen_user_count = max(self.seen_user_count, len(users))
            return events
        # A changed body or shifted absolute position is NOT a new send. Keep a
        # high-water mark across temporary empty/short accessibility snapshots.
        # The surrounding plug-in resets this tracker when changing conversations.
        new_users = ([users[-1]] if users[-1].identity not in self.seen_user_ids else []) if has_ids else users[self.seen_user_count:]
        if (not has_ids and users and not new_users and old.messages
                and old.messages[-1].role == 'assistant' and snapshot.messages[-1].role == 'user'):
            new_users = [users[-1]]
        self.seen_user_ids.update(m.identity for m in users if m.identity)
        if len(self.seen_user_ids) > 4096:
            self.seen_user_ids = {m.identity for m in users if m.identity}
        if new_users:
            if not has_ids:
                self.fallback_turn += 1
            for message in new_users:
                events.append(('user', message.text))
            self.seen_user_count = max(self.seen_user_count, len(users))
            self.pending = None
            self.offset = 0
        old_answers = [(i, m.text) for i, m in enumerate(old.messages) if m.role == 'assistant']
        old_latest = old_answers[-1] if old_answers else None
        same_identity = bool(latest and old_latest and snapshot.messages[latest[0]].identity == old.messages[old_latest[0]].identity)
        if latest and (latest != old_latest or not same_identity) and answer_key(latest) not in self.completed_answers:
            if self.pending is None or self.pending[0] != latest[0] or not latest[1].startswith(self.pending[1][:self.offset]):
                self.offset = 0
            self.pending = latest
            self.changed_at = now
        if snapshot.status and snapshot.status != self.last_status and now - self.status_at >= 1.5:
            events.append(('status', snapshot.status))
            self.last_status = snapshot.status
            self.status_at = now
        if self.pending and (not latest or self.pending != latest):
            self.pending = None
            self.offset = 0
        if self.pending:
            text = self.pending[1]
            idle = snapshot.busy is False
            quiet = now - self.changed_at
            finished = (idle and quiet >= delay) or (fallback > 0 and snapshot.busy is None and quiet >= fallback)
            if mode == 'progressive' and not finished:
                # Only enqueue completed paragraphs; never repeat an already spoken prefix.
                end = text.rfind('\n\n')
                if end > self.offset:
                    chunk = text[self.offset:end].strip()
                    if chunk:
                        events.append(('answer', chunk))
                    self.offset = end + 2
            if finished:
                chunk = text[self.offset:].strip() if mode == 'progressive' else text
                if chunk and answer_key(self.pending) not in self.completed_answers:
                    events.append(('answer', chunk))
                self.last_announced = self.pending
                self.completed_answers.add(answer_key(self.pending))
                if len(self.completed_answers) > 256:
                    self.completed_answers = {answer_key(self.pending)}
                self.pending = None
                self.offset = 0
        return events
