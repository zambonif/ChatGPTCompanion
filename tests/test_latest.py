"""Regression tests for rolling histories and editable fields inside old turns."""
import unittest
from test_engine import e

class LatestTests(unittest.TestCase):
    def test_editor_in_old_turn_does_not_hide_later_answer(self):
        tokens=[('heading','You said:','u1'),('text','old'),('edit','editing old text'),
                ('heading','ChatGPT said:','a1'),('text','Old answer'),
                ('heading','You said:','u2'),('text','new'),
                ('heading','ChatGPT said:','a2'),('text','Current answer'),('edit','composer')]
        s=e.parse_tokens(tokens)
        self.assertEqual(len(s.messages),4)
        self.assertEqual(s.messages[-1],e.Message('assistant','Current answer','a2'))

    def test_same_length_rolling_tail_announces_new_turn(self):
        t=e.Tracker()
        t.update(e.Snapshot((e.Message('user','Q','u1'),e.Message('assistant','A','a1'))),0)
        t.update(e.Snapshot((e.Message('assistant','A','a1'),e.Message('user','Q','u2'))),1)
        s=e.Snapshot((e.Message('user','Q','u2'),e.Message('assistant','A','a2')))
        t.update(s,2,fallback=3)
        self.assertEqual(t.update(s,6,fallback=3),[('answer','A')])

    def test_manual_cache_cleared_while_new_question_waits(self):
        t=e.Tracker()
        t.update(e.Snapshot((e.Message('user','Q','u1'),e.Message('assistant','Old','a1'))),0)
        t.update(e.Snapshot((e.Message('assistant','Old','a1'),e.Message('user','New question','u2'))),1)
        self.assertEqual(t.last_answer,'')

    def test_late_response_after_focus_gap(self):
        t=e.Tracker();t.update(e.Snapshot((e.Message('user','Q','u1'),)),0)
        # No snapshots are requested while a different window has focus.
        s=e.Snapshot((e.Message('user','Q','u1'),e.Message('assistant','New answer','a1')))
        t.update(s,60,fallback=3)
        self.assertEqual(t.update(s,64,fallback=3),[('answer','New answer')])

    def test_transient_empty_snapshot_recovers_without_old_speech(self):
        t=e.Tracker();s=e.Snapshot((e.Message('user','Q','u1'),e.Message('assistant','A','a1')))
        t.update(s,0);t.update(e.Snapshot(),1)
        self.assertEqual(t.last_answer,'')
        self.assertEqual(t.update(s,4,fallback=3),[])
        self.assertEqual(t.update(s,8,fallback=3),[])

if __name__=='__main__':unittest.main()
