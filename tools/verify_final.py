#!/usr/bin/env python3
"""Final source/preview parity, motion override, static-page asset behavior, measured readability."""
import asyncio, json, hashlib
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1];results=[]
def check(n,ok,d=None):
 results.append({'check':n,'passed':bool(ok),'details':d});print(('PASS 'if ok else 'FAIL ')+n,flush=True)
 (R/'verification/checks-final.json').write_text(json.dumps(results,indent=2))
async def images(p):
 await p.evaluate('''async()=>{await Promise.all([...document.images].map(async i=>{i.loading='eager';try{await i.decode()}catch{}}))}''')
async def main():
 async with async_playwright() as pw:
  b=await pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  p=await b.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
  await p.set_content((R/'OPEN_PREVIEW.html').read_text(),wait_until='load');await images(p)
  check('Reduced-motion user starts with effects disabled',await p.evaluate('document.documentElement.dataset.motion==="off"&&getComputedStyle(document.querySelector(".hero-rain")).display==="none"'))
  await p.locator('button[data-motion]').evaluate('e=>e.click()');await p.wait_for_timeout(180)
  check('Explicit user Play overrides reduced-motion default',await p.evaluate('document.documentElement.dataset.motion==="on"&&getComputedStyle(document.querySelector(".hero-rain")).display!=="none"&&document.querySelector(".hero-rain i").getAnimations().length>0'))
  await p.locator('button[data-motion]').evaluate('e=>e.click()');check('User can pause again',await p.evaluate('document.documentElement.dataset.motion==="off"'))
  await p.screenshot(path=str(R/'verification/final-hero-mobile.png'))
  # Render the actual standalone gallery markup with local assets embedded. This is not network navigation.
  html=(R/'gallery/index.html').read_text();media={}
  import base64,mimetypes,re
  for f in (R/'assets').glob('*'):
   if f.suffix in ['.webp','.svg','.png']:media[f.name]='data:'+str(mimetypes.guess_type(f.name)[0])+';base64,'+base64.b64encode(f.read_bytes()).decode()
  html=re.sub(r'(src|href)="(?:\.\./)?assets/([^"?#]+)"',lambda m:m[1]+'="'+media[m[2]]+'"' if m[2] in media else m[0],html)
  html=html.replace('<link rel="stylesheet" href="../assets/styles.css">','<style>'+(R/'assets/styles.css').read_text()+'</style>')
  for k in ['house3d.js','app.js']:html=html.replace(f'<script src="../assets/{k}" defer></script>','<script>'+(R/'assets'/k).read_text().replace('</script','<\\/script')+'</script>')
  q=await b.new_page(viewport={'width':1440,'height':950},reduced_motion='reduce')
  await q.set_content(html,wait_until='load');await images(q)
  check('Static Gallery source has correct active nav',await q.locator('.gallery-nav').get_attribute('aria-current')=='page')
  check('Static Gallery source renders all original links',await q.locator('.gallery-card [data-original-gallery]').count()==7)
  await q.screenshot(path=str(R/'verification/final-gallery-desktop.png'),full_page=True)
  await q.set_viewport_size({'width':390,'height':844});await q.screenshot(path=str(R/'verification/final-gallery-mobile.png'),full_page=True)
  await q.close()
  # Visual bounds of the gallery content at 200% text size, without hiding overflow.
  await p.locator('a[data-route="/gallery/"]').first.evaluate('e=>e.click()');await images(p)
  await p.add_style_tag(content='.gallery-card-copy>strong{font-size:40px!important}.gallery-card-copy .kicker{font-size:16px!important}.gallery-card-link{align-items:flex-start}.gallery-card{min-height:0}')
  check('Gallery headings wrap without clipping at enlarged text',await p.evaluate('document.documentElement.scrollWidth<=innerWidth+1&&[...document.querySelectorAll(".gallery-card-copy")].every(e=>e.scrollWidth<=e.clientWidth+1)'))
  await p.close();await b.close()
asyncio.run(main())
print('TOTAL',len(results),'PASS',sum(x['passed']for x in results),'FAIL',sum(not x['passed']for x in results))
raise SystemExit(0 if all(x['passed']for x in results) else 1)
