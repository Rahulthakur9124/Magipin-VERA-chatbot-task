import json, glob, os
from bot import compose

ROOT = os.path.dirname(__file__)
DATA = os.path.join(ROOT, 'expanded')

def load_dir(folder):
    out={}
    for p in glob.glob(os.path.join(DATA, folder, '*.json')):
        d=json.load(open(p, encoding='utf-8'))
        if folder == 'merchants': key=d.get('merchant_id')
        elif folder == 'customers': key=d.get('customer_id')
        elif folder == 'triggers': key=d.get('id')
        else: key=d.get('id')
        out[key]=d
    return out

cats={}
for p in glob.glob(os.path.join(DATA,'categories','*.json')):
    d=json.load(open(p, encoding='utf-8')); cats[d['slug']]=d
merchants=load_dir('merchants'); customers=load_dir('customers'); triggers=load_dir('triggers')
pairs=json.load(open(os.path.join(DATA,'test_pairs.json'), encoding='utf-8'))['pairs']

out=[]
for pair in pairs:
    m=merchants[pair['merchant_id']]
    t=triggers[pair['trigger_id']]
    c=customers.get(pair['customer_id']) if pair.get('customer_id') else None
    cat=cats[m['category_slug']]
    r=compose(cat,m,t,c)
    out.append({'test_id':pair['test_id'], **{k:r[k] for k in ('body','cta','send_as','suppression_key','rationale')}})

with open(os.path.join(ROOT,'submission.jsonl'),'w',encoding='utf-8') as f:
    for row in out: f.write(json.dumps(row, ensure_ascii=False)+'\n')
print(f'generated {len(out)} submissions')
