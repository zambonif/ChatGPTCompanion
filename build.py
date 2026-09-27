#!/usr/bin/env python3
"""Build with Python 3.11+ and the standard library only: python build.py."""
from pathlib import Path
import ast
import gettext
import html
import json
import re
import struct
import zipfile

ROOT = Path(__file__).resolve().parent
ADDON = ROOT / 'addon'
VERSION = '0.1.3'


def make_mo(messages):
    pairs = sorted((a.encode('utf-8'), b.encode('utf-8')) for a, b in messages.items())
    n = len(pairs)
    originals = b''.join(a + b'\0' for a, b in pairs)
    translated = b''.join(b + b'\0' for a, b in pairs)
    start = 28 + 16 * n
    data = struct.pack('<7I', 0x950412de, 0, n, 28, 28 + 8*n, 0, 0)
    offset = start
    for a, _ in pairs:
        data += struct.pack('<2I', len(a), offset)
        offset += len(a) + 1
    offset = start + len(originals)
    for _, b in pairs:
        data += struct.pack('<2I', len(b), offset)
        offset += len(b) + 1
    return data + originals + translated


def render_doc(source, lang):
    out = ['<!doctype html>', '<html lang="' + lang.replace('_','-') + '"><head>',
           '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">',
           '<title>ChatGPT Companion — ' + VERSION + '</title>',
           '<style>body{font:1.1rem/1.6 system-ui,sans-serif;max-width:58rem;margin:2rem auto;padding:0 1rem}a{color:#0645ad}li{margin:.5rem 0}</style></head><body><main>']
    listing = False
    for paragraph in source.split('\n\n'):
        for line in paragraph.splitlines() if paragraph.startswith('- ') else [paragraph]:
            line = line.strip()
            if not line:
                continue
            text = html.escape(line.lstrip('# ') if line.startswith('#') else line[2:] if line.startswith('- ') else line)
            text = re.sub(r'(https://[^\s<]+)', r'<a href="\1">\1</a>', text)
            if line.startswith('- '):
                if not listing:
                    out.append('<ul>'); listing = True
                out.append('<li>' + text + '</li>')
            else:
                if listing:
                    out.append('</ul>'); listing = False
                tag = 'h2' if line.startswith('## ') else 'h1' if line.startswith('# ') else 'p'
                out.append('<' + tag + '>' + text.replace('\n','<br>') + '</' + tag + '>')
    if listing:
        out.append('</ul>')
    out.append('</main></body></html>')
    return '\n'.join(out)


def main():
    tree = ast.parse((ADDON / 'globalPlugins/fzChatGPTCompanion/__init__.py').read_text(encoding='utf-8'))
    strings = sorted({n.args[0].value for n in ast.walk(tree) if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Name) and n.func.id == '_' and n.args and isinstance(n.args[0], ast.Constant)})
    translations = json.loads((ROOT / 'translations/ui.json').read_text(encoding='utf-8'))
    descriptions = {
        'pt_BR': 'Lê mensagens enviadas, respostas e avisos acessíveis na conversa ativa do ChatGPT. Versão experimental.',
        'es': 'Lee mensajes enviados, respuestas y avisos accesibles en la conversación activa de ChatGPT. Versión experimental.',
        'fr': 'Lit les messages envoyés, les réponses et les informations accessibles dans la conversation ChatGPT active. Version expérimentale.',
        'it': 'Legge messaggi inviati, risposte e avvisi accessibili nella conversazione attiva di ChatGPT. Versione sperimentale.',
    }
    pot = ['msgid ""\nmsgstr ""\n"Content-Type: text/plain; charset=UTF-8\\n"\n']
    for msg in strings:
        pot.append('msgid ' + json.dumps(msg,ensure_ascii=False) + '\nmsgstr ""\n')
    (ROOT / 'translations/messages.pot').write_text('\n'.join(pot), encoding='utf-8')
    for lang, values in translations.items():
        if not isinstance(values, dict) or set(values) != set(strings):
            raise ValueError('Translation count mismatch: ' + lang)
        header = 'Project-Id-Version: ChatGPT Companion '+VERSION+'\nLanguage: '+lang+'\nContent-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n'
        messages = {'': header}
        for msgid in strings:
            msgstr = values[msgid]
            if set(re.findall(r'\{\w+\}',msgid)) != set(re.findall(r'\{\w+\}',msgstr)):
                raise ValueError('Translation placeholder mismatch: ' + lang)
            messages[msgid] = msgstr
        folder = ADDON / 'locale' / lang / 'LC_MESSAGES'
        folder.mkdir(parents=True,exist_ok=True)
        (folder/'nvda.mo').write_bytes(make_mo(messages))
        po = '\n\n'.join('msgid '+json.dumps(a,ensure_ascii=False)+'\nmsgstr '+json.dumps(b,ensure_ascii=False) for a,b in messages.items())
        (folder/'nvda.po').write_text(po+'\n',encoding='utf-8')
        (folder.parent/'manifest.ini').write_text('summary = "ChatGPT Companion"\ndescription = "'+descriptions[lang]+'"\n',encoding='utf-8')
        with (folder/'nvda.mo').open('rb') as f:
            catalog = gettext.GNUTranslations(f)
        assert all(catalog.gettext(a)==b for a,b in messages.items() if a)
    for lang in ['en','pt_BR','es','fr','it']:
        source = (ROOT/'docs'/(lang+'.md')).read_text(encoding='utf-8')
        folder = ADDON/'doc'/lang
        folder.mkdir(parents=True,exist_ok=True)
        (folder/'readme.html').write_text(render_doc(source,lang),encoding='utf-8')
        (folder/'readme.txt').write_text(source,encoding='utf-8')
    dist = ROOT/'dist';dist.mkdir(exist_ok=True)
    target = dist/('ChatGPTCompanion-'+VERSION+'.nvda-addon')
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
        for f in sorted(ADDON.rglob('*')):
            if f.is_file() and '__pycache__' not in f.parts:
                info=zipfile.ZipInfo(f.relative_to(ADDON).as_posix(),(2026,9,27,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                archive.writestr(info,f.read_bytes())
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert 'manifest.ini' in z.namelist()
        assert z.read('manifest.ini').isascii()
    print(target)
    print('Validated 4 complete gettext catalogs, 5 documentation languages and English root manifest.')

if __name__=='__main__':main()
