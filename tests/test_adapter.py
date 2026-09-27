"""Exercise real field adapter functions with synthetic NVDA ControlField streams.
These are unit tests, not claims of live Windows accessibility testing.
"""
import ast
from pathlib import Path
from types import SimpleNamespace as NS
import unittest
from test_engine import e
source = Path(__file__).resolve().parents[1]/'addon/globalPlugins/fzChatGPTCompanion/__init__.py'
tree = ast.parse(source.read_text(encoding='utf-8'))
functions = ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'role_name','field_tokens','announcement_text'}],type_ignores=[])
namespace = {'_': lambda text: text}
exec(compile(functions,str(source),'exec'),namespace)
extract = namespace['field_tokens']
def start(role,name=''):
    return NS(command='controlStart',field={'role': NS(name=role),'name':name})
def end():
    return NS(command='controlEnd',field={})

class AdapterTests(unittest.TestCase):
    def test_sent_speech_settings(self):
        for read, confirm, expected in [(True, True, 'You said: hello'),
                (True, False, 'You said: hello'), (False, True, 'Message sent.'),
                (False, False, None)]:
            settings={'readSent':read,'confirmSent':confirm,'readAnswers':True,'readStatus':True}
            self.assertEqual(namespace['announcement_text']('user','hello',settings),expected)

    def test_mutations_stay_silent_after_settings_change(self):
        tracker=e.Tracker(); tracker.update(e.Snapshot(),0)
        muted={'readSent':False,'confirmSent':False,'readAnswers':True,'readStatus':True}
        events=tracker.update(e.Snapshot((e.Message('user','hello'),),True),1)
        self.assertEqual([namespace['announcement_text'](k,t,muted) for k,t in events],[None])
        # Enabling sent reading later must not replay that already handled send.
        self.assertEqual(tracker.update(e.Snapshot((e.Message('user','hello\nThinking 2 s'),),True),2),[])

    def test_nested_heading_and_buttons(self):
        fields=[start('DOCUMENT'),start('HEADING'),start('STATICTEXT'),'Você disse:',end(),end(),
            'Oi',start('HEADING', 'O ChatGPT disse:'),end(),start('PARAGRAPH'),'Olá!',end(),
            start('BUTTON', 'Copiar'),end(),start('EDITABLETEXT'),'unsent draft',end(),
            start('BUTTON','Enviar mensagem'),end(),end()]
        snapshot=e.parse_tokens(extract(fields))
        self.assertEqual(snapshot.messages,(e.Message('user','Oi'),e.Message('assistant','Olá!')))
        self.assertIs(snapshot.busy,False)

    def test_status_is_separate_from_answer(self):
        fields=[start('HEADING'),'ChatGPT said:',end(),start('STATUSBAR'),'Searching three sources',end(),
            start('PARAGRAPH'),'The answer.',end(),start('BUTTON'),'Stop generating',end()]
        snapshot=e.parse_tokens(extract(fields))
        self.assertEqual(snapshot.status,'Searching three sources')
        self.assertEqual(snapshot.messages,(e.Message('assistant','The answer.'),))
        self.assertIs(snapshot.busy,True)

    def test_paragraph_boundaries_preserved(self):
        fields=[start('HEADING'),'ChatGPT said:',end(),start('PARAGRAPH'),'One.',end(),start('PARAGRAPH'),'Two.',end()]
        snapshot=e.parse_tokens(extract(fields))
        self.assertEqual(snapshot.messages[0].text,'One.\n\nTwo.')

    def test_formatting_does_not_become_speech(self):
        fields=[start('HEADING'),'ChatGPT said:',end(),NS(command='formatChange',field={'bold':True}),'Answer.']
        self.assertEqual(e.parse_tokens(extract(fields)).messages[0].text,'Answer.')

if __name__=='__main__': unittest.main()
