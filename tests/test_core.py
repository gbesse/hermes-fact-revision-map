import unittest,copy,json
from hermes_fact_revision_map import run
DEMO={'facts': [{'id': 'supplier-lead-time', 'revision': 2}], 'documents': [{'id': 'plan', 'reads': [{'fact': 'supplier-lead-time', 'revision': 1}]}, {'id': 'draft', 'depends_on_documents': ['plan']}, {'id': 'independent'}]}
class DomainTests(unittest.TestCase):
 def test_revision_correction_cascades(self):
  x=run(DEMO);self.assertEqual([r['document']for r in x['review_plan']],['plan','draft']);self.assertEqual(x['unaffected_document_ids'],['independent']);self.assertFalse(x['documents_modified'])
 def test_current_read_is_not_stale(self):
  x=copy.deepcopy(DEMO);x['documents'][0]['reads'][0]['revision']=2;self.assertEqual(run(x)['review_plan'],[])
 def test_dependency_cycle(self):
  x=copy.deepcopy(DEMO);x['documents'][0]['depends_on_documents']=['draft']
  with self.assertRaises(ValueError):run(x)
