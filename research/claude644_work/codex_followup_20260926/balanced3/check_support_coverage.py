"""Supplement exact region checker with support-union coverage and a certificate digest."""
import hashlib,json,sys
from pathlib import Path
SRC=Path('/Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/capture/b3c')
sys.path.insert(0,str(SRC))
import b4core as bc
pairdata=json.loads((SRC.parent/'heavy/astra_support_capacity_minimal.json').read_text())
for f in sys.argv[1:]:
 path=Path(f); data=json.loads(path.read_text()); count=0; seen=set(); maxwin=0
 def walk(node):
  global count,maxwin
  if node['k'] in ('TMPL','FACET'):
   cells,assignment=bc.template_support(node['t'],pairdata)
   union=0
   for cell in cells: union |= cell
   assert union==127, ('missing row; dual may be unbounded',cells)
   assert bc.is_bad_support(cells)
   assert len(assignment)==7
   maxwin=max(maxwin,max(sum(bool(cell & (1<<j)) for cell in cells) for j in range(7)))
   seen.add(tuple(cells));count+=1
  for child in node.get('kids',[]):
   walk(child[1] if isinstance(child,list) else child)
 walk(data['tree'])
 print('SUPPORT_COVERAGE_PASS',path.name,'template_nodes',count,'supports',len(seen),'max_window_parents',maxwin,'sha256',hashlib.sha256(path.read_bytes()).hexdigest())
