"""Exercise tail range selection with a simulated NVDA TextInfo provider."""
import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace as NS
import unittest
from unittest.mock import patch
from test_engine import e
from test_adapter import extract,start,end

class Range:
    def __init__(self,doc,start=0,finish=None):
        self.doc=doc;self.start=start;self.finish=len(doc.data) if finish is None else finish
    def collapse(self,end=False):
        if end:self.start=self.finish
        else:self.finish=self.start
    def copy(self):return Range(self.doc,self.start,self.finish)
    def setEndPoint(self,other,which):
        assert which=='endToEnd';self.finish=other.finish
    @property
    def text(self):
        self.doc.text_requests.append((self.start,self.finish))
        if self.finish-self.start>1000:raise AssertionError('Requested whole historical text')
        return self.doc.data[self.start:self.finish]
    def getTextWithFields(self):
        self.doc.field_requests.append((self.start,self.finish))
        assert self.finish-self.start<1000, 'Retrieved old history'
        return self.doc.fields
    def move(self,unit,count,endPoint=None):
        assert unit=='line' and endPoint=='start'
        self.start=self.doc.tail_start
        return -5

class Doc:
    def __init__(self,indexed=True):
        self.tail_start=300001
        self.data='x'*self.tail_start+'You said: question\nChatGPT said: current'
        self.text_requests=[];self.field_requests=[]
        self.fields=[start('HEADING'),'You said:',end(),'question',start('HEADING'),'ChatGPT said:',end(),'current']
        if not indexed:self._iterNodesByType=None
    def makeTextInfo(self,position):
        assert position=='all';return Range(self)
    def _iterNodesByType(self,kind,direction,pos):
        assert direction=='previous'
        for name in ['ChatGPT said:','You said:']:
            at=self.data.rfind(name)
            yield NS(textInfo=Range(self,at,at+len(name)))

class ReadingTests(unittest.TestCase):
    def setUp(self):
        path=Path(__file__).resolve().parents[1]/'addon/globalPlugins/fzChatGPTCompanion/reading.py'
        spec=importlib.util.spec_from_file_location('reader_test.reading',path)
        self.reader=importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules,{'reader_test':ModuleType('reader_test'),'reader_test.engine':e,
                                    'textInfos':NS(POSITION_ALL='all',UNIT_LINE='line')}):
            spec.loader.exec_module(self.reader)
    def test_300k_history_reads_only_latest_indexed_range(self):
        doc=Doc();s=self.reader.read_snapshot(doc,extract)
        self.assertEqual(s.messages[-1].text,'current')
        self.assertTrue(all(a>=doc.tail_start for a,b in doc.field_requests))
    def test_non_indexed_provider_uses_tail_lines(self):
        doc=Doc(False);s=self.reader.read_snapshot(doc,extract)
        self.assertEqual(s.messages[-1].text,'current')
        self.assertFalse(doc.text_requests)

if __name__=='__main__':unittest.main()
