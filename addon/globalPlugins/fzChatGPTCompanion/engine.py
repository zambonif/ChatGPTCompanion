# Copyright (C) 2026 Fernando de Paula Zamboni
# SPDX-License-Identifier: GPL-2.0-or-later
"""Pure conversation extraction and announcement state machine (no NVDA imports)."""
from dataclasses import dataclass
import re
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


@dataclass(frozen=True)
class Snapshot:
    messages: tuple = ()
    busy: object = None  # True: stop control; False: send control; None: unknown.
    status: str = ''


def parse_tokens(tokens, ignore_interface=True):
    """Actor boundaries must be actual accessibility headings, not arbitrary text."""
    messages, body = [], []
    actor = None
    stop = send = False
    status = ''
    composer = False
    def flush():
        if actor:
            text = re.sub(r'[ \t]+', ' ', ''.join(body))
            text = re.sub(r'\n{3,}', '\n\n', text).strip()
            if text:
                messages.append(Message(actor, text))
    for kind, text in tokens:
        name = normalized(text)
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
        if kind == 'heading' and name in USER_HEADINGS | ASSISTANT_HEADINGS:
            flush()
            actor = 'user' if name in USER_HEADINGS else 'assistant'
            body = []
        elif kind == 'heading' and any(name.startswith(p) for p in PROGRESS):
            status = text.strip()
        elif actor:
            body.append(('\n' + text + '\n') if kind == 'heading' else text)
    flush()
    if ignore_interface and actor == 'assistant' and messages and messages[-1].role == 'assistant':
        cleaned = strip_interface_footer(messages[-1].text)
        if cleaned:
            messages[-1] = Message('assistant', cleaned)
        else:
            messages.pop()
    return Snapshot(tuple(messages), True if stop else False if send else None, status)


class Tracker:
    """Keep only one foreground conversation; baseline prevents reading old history."""
    def __init__(self):
        self.previous = None
        self.seen_user_count = 0
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
        self.previous = snapshot
        answers = [(i, m.text) for i, m in enumerate(snapshot.messages) if m.role == 'assistant']
        latest = answers[-1] if answers else None
        if latest:
            self.last_answer = latest[1]
        # Once another user turn exists, the preceding answer is historical.
        # Its disappearing footer or reflow must not queue it as a new answer.
        last_user = max((i for i, m in enumerate(snapshot.messages) if m.role == 'user'), default=-1)
        if latest and latest[0] < last_user:
            latest = None
        def answer_key(entry):
            index, text = entry
            turn = sum(m.role == 'user' for m in snapshot.messages[:index])
            return (turn, ' '.join(text.split()))
        users = [m for m in snapshot.messages if m.role == 'user']
        if old is None:
            self.seen_user_count = len(users)
            self.last_status = snapshot.status
            self.completed_answers.update(answer_key(entry) for entry in answers)
            return events
        # A shrinking history is likely navigation/virtualisation: establish a new baseline.
        if len(snapshot.messages) < len(old.messages):
            self.pending = None
            self.offset = 0
            self.seen_user_count = max(self.seen_user_count, len(users))
            return events
        # A changed body or shifted absolute position is NOT a new send. Keep a
        # high-water mark across temporary empty/short accessibility snapshots.
        # The surrounding plug-in resets this tracker when changing conversations.
        if len(users) > self.seen_user_count:
            for message in users[self.seen_user_count:]:
                events.append(('user', message.text))
            self.seen_user_count = len(users)
            self.pending = None
            self.offset = 0
        old_answers = [(i, m.text) for i, m in enumerate(old.messages) if m.role == 'assistant']
        old_latest = old_answers[-1] if old_answers else None
        if latest and latest != old_latest and answer_key(latest) not in self.completed_answers:
            if self.pending is None or self.pending[0] != latest[0] or not latest[1].startswith(self.pending[1][:self.offset]):
                self.offset = 0
            self.pending = latest
            self.changed_at = now
        if snapshot.status and snapshot.status != self.last_status and now - self.status_at >= 1.5:
            events.append(('status', snapshot.status))
            self.last_status = snapshot.status
            self.status_at = now
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
                self.pending = None
                self.offset = 0
        return events
