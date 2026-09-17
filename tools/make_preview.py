#!/usr/bin/env python3
"""Create a single-file, network-independent review of the exact built pages."""
from pathlib import Path
import re,json,base64,mimetypes
R=Path(__file__).resolve().parents[1]
media={}
for p in (R/'assets').iterdir():
    if p.suffix.lower() not in {'.svg','.webp','.png','.jpg','.jpeg'}: continue
    mime=mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
    media[p.name]='data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode('ascii')
pages=json.loads((R/'tools/preview-pages.json').read_text())
# Keep per-route markup asset paths in the route registry; runtime resolves against shared media.
text=(R/'index.html').read_text()
text=re.sub(r'(src|href)="(?:\./)?assets/([^"?#]+)"',lambda m:f'{m[1]}="{media[m[2]]}"' if m[2] in media else m[0],text)
css=(R/'assets/styles.css').read_text()
text=text.replace('<link rel="stylesheet" href="assets/styles.css">','<style>'+css+'</style>')
# Even when production is configured, the downloaded review remains a noindex artifact.
text=re.sub(r'<meta name="robots"[^>]+>','<meta name="robots" content="noindex, nofollow">',text)
text=re.sub(r'<link rel="canonical"[^>]+>','',text)
jsafe=lambda s: s.replace('</script','<\\/script')
payload='window.W360_PAGES='+json.dumps(pages,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';window.W360_MEDIA='+json.dumps(media,separators=(',',':'))+';window.W360_ROUTE="/";'
text=text.replace('<script src="assets/house3d.js" defer></script>','<script>'+payload+'</script><script>'+jsafe((R/'assets/house3d.js').read_text())+'</script>')
text=text.replace('<script src="assets/app.js" defer></script>','<script>'+jsafe((R/'assets/app.js').read_text())+'</script>')
(R/'OPEN_PREVIEW.html').write_text(text)
print('Preview generated:',len(text.encode()),'bytes;',len(pages),'routes;',len(media),'embedded images/icons.')
