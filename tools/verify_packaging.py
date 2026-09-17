#!/usr/bin/env python3
"""Check deployable-path configuration and offline preview parity in a scratch copy."""
from pathlib import Path
import tempfile,shutil,subprocess,sys,json,re,hashlib
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1];checks=[]
def record(n,ok,d=None):checks.append({'check':n,'passed':bool(ok),'details':d});print(('PASS 'if ok else'FAIL ')+n)
source=json.loads((R/'tools/preview-pages.json').read_text());preview=(R/'OPEN_PREVIEW.html').read_text()
embedded=json.loads(re.search(r'window.W360_PAGES=(.*?);window.W360_MEDIA=',preview,re.S).group(1))
for route,v in source.items():record('Preview exactly matches source route '+route,embedded.get(route)==v)
soup=BeautifulSoup(preview,'html.parser');requests=[e.get('src') or e.get('href') for e in soup.select('script[src],img[src],link[rel=stylesheet]') if not (e.get('src') or e.get('href')).startswith('data:')]
record('Offline preview embeds all initial runtime dependencies',not requests,requests)
record('Preview metadata cannot be indexed',soup.select_one('meta[name=robots]')['content']=='noindex, nofollow')
with tempfile.TemporaryDirectory(prefix='w360-config-test-') as t:
 root=Path(t)/'site';shutil.copytree(R,root,ignore=shutil.ignore_patterns('verification','OPEN_PREVIEW.html','MANIFEST.json','*.zip','__pycache__'))
 c=subprocess.run([sys.executable,str(root/'tools/configure_site.py'),'--url','https://example.org/property-preview','--index'],capture_output=True,text=True)
 record('Production configuration completes in scratch copy',c.returncode==0,c.stderr or None)
 pages=list((root/'services').rglob('index.html'))+list((root/'blog').rglob('index.html'))+[root/'index.html',root/'contact/index.html',root/'gallery/index.html']
 ok=True
 for p in pages:
  h=BeautifulSoup(p.read_text(),'html.parser');can=h.select_one('link[rel=canonical]');ok=ok and can is not None and can['href'].startswith('https://example.org/property-preview/') and h.select_one('meta[name=robots]')['content'].startswith('index,')
 record('All 18 production pages use configured origin and indexability',ok)
 urls=re.findall(r'<loc>(.*?)</loc>',(root/'sitemap.xml').read_text());record('Sitemap has 18 absolute configured URLs',len(urls)==18 and all(x.startswith('https://example.org/property-preview/') for x in urls))
 h=BeautifulSoup((root/'OPEN_PREVIEW.html').read_text(),'html.parser');record('Offline review remains noindex after production build','noindex' in h.select_one('meta[name=robots]')['content'])
 record('GitHub project-relative asset paths retained','../../assets/styles.css' in (root/'services/foundation-leaks/index.html').read_text())
 for bad in ['http://example.org','https://example.org/?private=token','https://name:secret@example.org']:
  c=subprocess.run([sys.executable,str(root/'tools/configure_site.py'),'--url',bad,'--index'],capture_output=True,text=True)
  record('Invalid production URL is rejected '+bad.replace('name:secret','credentials'),c.returncode!=0)
record('Original source indexing stays disabled',json.loads((R/'content/settings.json').read_text())['indexable'] is False)
(R/'verification/checks-packaging.json').write_text(json.dumps(checks,indent=2))
sys.exit(not all(x['passed']for x in checks))
