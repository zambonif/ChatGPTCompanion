"""Run real plugin methods with simulated NVDA dependencies (no Windows claims)."""
from collections import OrderedDict
from pathlib import Path
from types import SimpleNamespace as NS, ModuleType
import sys
import unittest
from unittest.mock import patch
from test_engine import e

class Base:
    def __init__(self,*a,**k):pass
    def terminate(self):pass

class PluginTests(unittest.TestCase):
    def setUp(self):
        self.messages=[]
        self.settings={'enabled':True,'readSent':False,'confirmSent':False,'readAnswers':True,
            'readStatus':False,'ignoreInterface':True,'mode':'complete','settleSeconds':2,'fallbackSeconds':3}
        class Conf(dict):pass
        conf=Conf(fzChatGPTCompanion=self.settings);conf.spec={}
        gui=ModuleType('gui');gui.guiHelper=NS()
        mods={
            'addonHandler':NS(initTranslation=lambda:None),'api':NS(),'config':NS(conf=conf),
            'controlTypes':NS(Role=NS(DOCUMENT='document')),'globalPluginHandler':NS(GlobalPlugin=Base),
            'globalVars':NS(appArgs=NS(secure=False)),'gui':gui,
            'gui.settingsDialogs':NS(SettingsPanel=Base,NVDASettingsDialog=NS(categoryClasses=[])),
            'scriptHandler':NS(script=lambda **kw:lambda f:f),'textInfos':NS(),
            'ui':NS(message=self.messages.append),'wx':NS(CallLater=lambda *a:NS(Stop=lambda:None)),
            'runtime.engine':e,'runtime.reading':NS(read_snapshot=lambda *a:None),
        }
        ns={'__name__':'runtime.plugin','__package__':'runtime','_':lambda s:s}
        path=Path(__file__).resolve().parents[1]/'addon/globalPlugins/fzChatGPTCompanion/__init__.py'
        with patch.dict(sys.modules,mods):exec(compile(path.read_text(),str(path),'exec'),ns)
        self.ns=ns;self.plugin=ns['GlobalPlugin']()
        self.root=NS(processID=100,windowHandle=10)
        self.context=(object(),self.root,'https://chatgpt.com/c/one','chrome')
        self.current=e.Snapshot((e.Message('user','Q','u1'),))
        ns['document_context']=lambda:self.context
        ns['read_snapshot']=lambda *args:self.current
        self.clock=0;ns['time']=NS(monotonic=lambda:self.clock)

    def tearDown(self):self.plugin.terminate()

    def test_auto_response_after_leaving_and_returning(self):
        self.plugin._tick()
        context=self.context;self.context=None;self.clock=1;self.plugin._tick()
        self.current=e.Snapshot((e.Message('user','Q','u1'),e.Message('assistant','fresh','a1')))
        self.context=context;self.clock=10;self.plugin._tick()
        self.clock=14;self.plugin._tick()
        self.assertEqual(self.messages,['ChatGPT: fresh'])

    def test_manual_uses_current_text_not_cached_old_answer(self):
        self.current=e.Snapshot((e.Message('assistant','old','a1'),));self.plugin._tick()
        self.current=e.Snapshot((e.Message('assistant','current','a2'),))
        self.plugin.script_repeat(None)
        self.assertEqual(self.messages,['current'])

    def test_manual_does_not_fall_back_to_previous_answer_on_failure(self):
        self.current=e.Snapshot((e.Message('assistant','old','a1'),));self.plugin._tick()
        def fail(*a):raise RuntimeError('provider unavailable')
        self.ns['read_snapshot']=fail
        self.plugin.script_repeat(None)
        self.assertEqual(self.messages,['No answer available.'])

    def test_manual_does_not_repeat_old_answer_while_new_user_waits(self):
        self.current=e.Snapshot((e.Message('assistant','old','a1'),e.Message('user','new','u2')))
        self.plugin.script_repeat(None)
        self.assertEqual(self.messages,['No answer available.'])

    def test_different_windows_same_url_keep_separate_trackers(self):
        self.plugin._tick();first=self.plugin.tracker
        self.context=(object(),NS(processID=100,windowHandle=20),self.context[2],'chrome')
        self.plugin._tick();self.assertIsNot(self.plugin.tracker,first)
        self.assertEqual(len(self.plugin.sessions),2)

    def test_manual_still_works_when_monitoring_is_disabled(self):
        self.settings['enabled']=False
        self.current=e.Snapshot((e.Message('assistant','fresh','a2'),))
        self.plugin.script_repeat(None)
        self.assertEqual(self.messages,['fresh'])

if __name__=='__main__':unittest.main()
