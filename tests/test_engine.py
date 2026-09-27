import importlib.util
from pathlib import Path
import sys
import unittest
p = Path(__file__).resolve().parents[1] / 'addon/globalPlugins/fzChatGPTCompanion/engine.py'
spec = importlib.util.spec_from_file_location('engine', p)
e = importlib.util.module_from_spec(spec)
sys.modules['engine'] = e
spec.loader.exec_module(e)
M, S, T = e.Message, e.Snapshot, e.Tracker

class EngineTests(unittest.TestCase):
    def test_domain_scope(self):
        for u in ['https://chatgpt.com/c/1','https://chat.openai.com/']:
            self.assertTrue(e.allowed_url(u))
        for u in ['https://chatgpt.com.evil.test', 'https://evil.test/chatgpt.com', 'file:///chatgpt.com', 'http://chatgpt.com', 'https://chatgpt.com@evil.test']:
            self.assertFalse(e.allowed_url(u))

    def test_multilingual_heading_boundaries(self):
        for user, bot in [('You said:', 'ChatGPT said:'), ('Você disse:', 'O ChatGPT disse:'), ('Dijiste:', 'ChatGPT dijo:'), ('Vous avez dit :', 'ChatGPT a dit :'), ('Hai detto:', 'ChatGPT ha detto:')]:
            s=e.parse_tokens([('text','sidebar'),('edit','search'),('heading',user),('text','hello'),('heading',bot),('text','reply'),('button','Copy'),('edit','draft secret'),('text','disclaimer'),('button','Send message')])
            self.assertEqual(s.messages,(M('user','hello'),M('assistant','reply')))
            self.assertIs(s.busy,False)

    def test_plain_text_does_not_impersonate_actor(self):
        s=e.parse_tokens([('heading','You said:'),('text','ChatGPT said:\nthis is user text')])
        self.assertEqual(len(s.messages),1)
        self.assertEqual(s.messages[0].role,'user')

    def test_baseline_is_silent(self):
        t=T(); s=S((M('user','old'),M('assistant','old answer')),False)
        self.assertEqual(t.update(s,0),[])
        self.assertEqual(t.update(s,10),[])
        self.assertEqual(t.last_answer,'old answer')

    def test_send_only_when_message_exists(self):
        t=T();t.update(S(),0)
        self.assertEqual(t.update(S((M('user','Hi'),),True),1),[('user','Hi')])
        self.assertEqual(t.update(S((M('user','Hi'),),True),2),[])

    def test_response_waits_for_idle(self):
        t=T();t.update(S(),0)
        s=S((M('user','Hi'),M('assistant','Answer')),True)
        t.update(s,1)
        self.assertEqual(t.update(s,50),[])
        done=S(s.messages,False)
        self.assertEqual(t.update(done,51),[('answer','Answer')])
        self.assertEqual(t.update(done,52),[])

    def test_no_inferred_completion_by_default(self):
        t=T();t.update(S(),0)
        s=S((M('assistant','Partial'),),None)
        t.update(s,1)
        self.assertEqual(t.update(s,100),[])
        self.assertEqual(t.update(s,101,fallback=8),[('answer','Partial')])

    def test_progressive_no_repetition(self):
        t=T();t.update(S(),0)
        self.assertEqual(t.update(S((M('assistant','One.\n\nTwo'),),True),1,mode='progressive'),[('answer','One.')])
        self.assertEqual(t.update(S((M('assistant','One.\n\nTwo.'),),True),2,mode='progressive'),[])
        self.assertEqual(t.update(S((M('assistant','One.\n\nTwo.'),),False),5,mode='progressive'),[('answer','Two.')])

    def test_progress_dedup_and_throttle(self):
        t=T();t.update(S(),0)
        self.assertEqual(t.update(S(status='Thinking'),1),[('status','Thinking')])
        self.assertEqual(t.update(S(status='Thinking'),2),[])
        self.assertEqual(t.update(S(status='Searching'),2),[])
        self.assertEqual(t.update(S(status='Searching'),3),[('status','Searching')])

    def test_same_user_text_twice(self):
        t=T();t.update(S((M('user','Hi'),M('assistant','Hello')),False),0)
        out=t.update(S((M('user','Hi'),M('assistant','Hello'),M('user','Hi')),True),1)
        self.assertEqual(out,[('user','Hi')])

    def test_history_shrink_baselines(self):
        t=T();t.update(S((M('user','old'),M('assistant','old answer')),False),0)
        self.assertEqual(t.update(S((M('assistant','different'),),False),1),[])

    def test_sent_message_mutation_is_not_another_send(self):
        t=T();t.update(S(),0)
        self.assertEqual(t.update(S((M('user','Question'),),True),1),[('user','Question')])
        for now, tail in enumerate(['\nThinking 1 s','\nThinking 2 s','', '\nSearching'],2):
            self.assertEqual(t.update(S((M('user','Question'+tail),),True),now),[])

    def test_old_user_text_changes_do_not_replay_latest_user(self):
        t=T();t.update(S((M('user','old'),M('assistant','answer'),M('user','new')),True),0)
        changed=S((M('user','old revised'),M('assistant','answer'),M('user','new')),True)
        self.assertEqual(t.update(changed,1),[])

    def test_transient_empty_snapshot_does_not_replay_sent_message(self):
        t=T();t.update(S(),0)
        t.update(S((M('user','Question'),),True),1)
        t.update(S(),2)
        self.assertEqual(t.update(S((M('user','Question'),),True),3),[])
        t.update(S((M('user','Question'),M('assistant','Answer')),True),4)
        events=t.update(S((M('user','Question'),M('assistant','Answer'),M('user','Question')),True),5)
        self.assertEqual(events,[('user','Question')])

    def test_user_position_changes_do_not_mean_new_send(self):
        t=T();t.update(S((M('user','one'),M('user','two')),True),0)
        out=t.update(S((M('user','one'),M('assistant','late answer'),M('user','two')),True),1)
        self.assertFalse(any(kind=='user' for kind,text in out))

    def test_stop_wins_over_send(self):
        self.assertIs(e.parse_tokens([('button','Send'),('button','Stop generating')]).busy,True)

if __name__=='__main__':unittest.main()
