from .common import unique_ids,identifier,integer
def run(data):
 facts=data['facts'];documents=data['documents']
 if len(facts)>1000 or len(documents)>1000:raise ValueError('size')
 unique_ids(facts);unique_ids(documents);current={r['id']:integer(r['revision'],1,10**9)for r in facts};docs={r['id']:r for r in documents};reasons={};dependencies={}
 for key,d in docs.items():
  deps=d.get('depends_on_documents',[])
  if not isinstance(deps,list)or len(deps)>1000 or any(p not in docs for p in deps):raise ValueError('document_dependency')
  dependencies[key]=deps
  for read in d.get('reads',[]):
   fact=identifier(read['fact']);revision=integer(read['revision'],1,10**9)
   if fact not in current:reasons.setdefault(key,[]).append({'code':'missing_fact','fact':fact})
   elif current[fact]!=revision:reasons.setdefault(key,[]).append({'code':'fact_revision_changed','fact':fact,'read_revision':revision,'current_revision':current[fact]})
 done=set();visiting=set();order=[]
 def visit(k,depth=0):
  if k in visiting or depth>200:raise ValueError('cycle_or_depth')
  if k in done:return
  visiting.add(k)
  for p in dependencies[k]:visit(p,depth+1)
  visiting.remove(k);done.add(k);order.append(k)
 for k in docs:visit(k)
 for k in order:
  for p in dependencies[k]:
   if p in reasons:reasons.setdefault(k,[]).append({'code':'dependent_document_stale','document':p})
 return {'review_plan':[{'document':k,'reasons':reasons[k]}for k in order if k in reasons],'unaffected_document_ids':[k for k in docs if k not in reasons],'documents_modified':False,'facts_rewritten':False}
