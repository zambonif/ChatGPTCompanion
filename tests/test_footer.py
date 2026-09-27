import unittest
from test_engine import e

WARNING='O ChatGPT pode cometer erros. Confira informações importantes.'
FOOTER=WARNING+'\nResposta mais recente'

def parse(answer, enabled=True, role='ChatGPT said:'):
    return e.parse_tokens([('heading',role),('text',answer)],ignore_interface=enabled)

class FooterTests(unittest.TestCase):
    def test_reported_footer_removed(self):
        self.assertEqual(parse('Minha resposta.\n'+FOOTER).messages[0].text,'Minha resposta.')

    def test_setting_off_preserves_footer(self):
        text='Minha resposta.\n'+FOOTER
        self.assertEqual(parse(text,False).messages[0].text,text)

    def test_single_sentence_at_answer_end_preserved(self):
        self.assertEqual(parse('Um aviso útil:\n'+WARNING).messages[0].text,'Um aviso útil:\n'+WARNING)

    def test_quote_and_middle_reference_preserved(self):
        for text in ['Ele disse: “'+FOOTER+'”','Exemplo:\n'+FOOTER+'\nA explicação continua.']:
            self.assertEqual(parse(text).messages[0].text,text)

    def test_user_message_never_filtered(self):
        self.assertEqual(parse(FOOTER,role='You said:').messages[0].text,FOOTER)

    def test_five_language_footer_pairs(self):
        for warning,label in e.FOOTERS:
            self.assertEqual(e.strip_interface_footer('Answer\n'+warning+'\n'+label),'Answer')

    def test_footer_only_has_no_spoken_message(self):
        self.assertEqual(parse(FOOTER).messages,())

    def test_footer_appearing_does_not_requeue_answer(self):
        tracker=e.Tracker(); tracker.update(e.Snapshot(),0)
        tracker.update(parse('Answer'),1,fallback=3)
        self.assertEqual(tracker.update(parse('Answer'),5,fallback=3),[('answer','Answer')])
        for now in [6,10,15]:
            self.assertEqual(tracker.update(parse('Answer\n'+FOOTER),now,fallback=3),[])

    def test_previous_answer_changes_after_new_user_stays_silent(self):
        tracker=e.Tracker()
        tracker.update(e.Snapshot((e.Message('user','old'),e.Message('assistant','Old answer\n'+FOOTER))),0)
        updated=e.Snapshot((e.Message('user','old'),e.Message('assistant','Old answer'),e.Message('user','new')))
        self.assertEqual(tracker.update(updated,1,fallback=3),[('user','new')])
        self.assertEqual(tracker.update(updated,5,fallback=3),[])
        new=e.Snapshot(updated.messages+(e.Message('assistant','New answer'),))
        tracker.update(new,6,fallback=3)
        self.assertEqual(tracker.update(new,10,fallback=3),[('answer','New answer')])

    def test_completed_answer_disappears_and_returns(self):
        tracker=e.Tracker();tracker.update(e.Snapshot(),0)
        snapshot=e.Snapshot((e.Message('user','question'),e.Message('assistant','Answer')))
        tracker.update(snapshot,1,fallback=3);tracker.update(snapshot,5,fallback=3)
        tracker.update(e.Snapshot(),6,fallback=3)
        self.assertEqual(tracker.update(snapshot,7,fallback=3),[])
        self.assertEqual(tracker.update(snapshot,11,fallback=3),[])

    def test_identical_answer_to_new_question_is_read(self):
        tracker=e.Tracker()
        snapshot=e.Snapshot((e.Message('user','question'),e.Message('assistant','Yes')))
        tracker.update(snapshot,0)
        new=e.Snapshot(snapshot.messages+(e.Message('user','again'),e.Message('assistant','Yes')))
        tracker.update(new,1,fallback=3)
        self.assertEqual(tracker.update(new,5,fallback=3),[('answer','Yes')])

if __name__=='__main__':unittest.main()
