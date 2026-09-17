#!/usr/bin/env python3
"""R4 additions: source-mapped galleries, small thumbnails, mobile navigation, hero motion.
Network links are tested with an intercepted fixture, never represented as live album rendering.
"""
import asyncio, json, hashlib, os
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1];V=R/'verification';out=[]
G=json.loads((R/'content/galleries.json').read_text())
EXPECTED={
 'foundation':'56a7973b-e50f-440c-bdc6-6422a0b36fa5',
 'drainage':'2e5380fd-7a44-44f1-a835-40a7d01db26d',
 'concrete':'112d32f1-3599-430e-8b67-2e4909d00ac7',
 'wetareas':'8150d1e7-aee6-42ce-b194-bdb09e2269fb',
 'cracks':'612c09a1-0427-446b-bc2b-ae3647c3028e',
 'underslab':'352ae15c-5af3-46db-bfbc-1b5232143eb6',
 'other':'db6d619c-9311-4db7-947a-1a1c67a12811'}
def check(n,ok,d=None):
 out.append({'check':n,'passed':bool(ok),'details':d});print(('PASS ' if ok else 'FAIL ')+n,flush=True)
 (V/('checks-r4-'+os.getenv('R4_GROUP','full')+'.json')).write_text(json.dumps(out,indent=2))
async def images(p):
 return await p.evaluate('''async()=>{await Promise.all([...document.images].map(async i=>{i.loading='eager';try{await i.decode()}catch{}}));return [...document.images].filter(i=>!i.naturalWidth).map(i=>i.alt)}''')
async def go(p,route):
 await p.evaluate("r=>{const a=document.createElement('a');a.dataset.route=r;a.href='#';document.body.append(a);a.click();a.remove();}",route)
 await p.wait_for_timeout(40)
async def bounds(p):return await p.evaluate('({w:innerWidth,doc:document.documentElement.scrollWidth,body:document.body.scrollWidth})')
# Source provenance is the seven original hrefs retrieved from the source homepage.
check('Seven original album IDs match independently recorded homepage hrefs',len(G)==7 and all(g['url']=='https://abraham311.editorx.io/services/set/'+EXPECTED[g['id']] for g in G))
check('Every original gallery destination is unique',len({g['url'] for g in G})==7)
soup=BeautifulSoup((R/'gallery/index.html').read_text(),'html.parser')
check('Gallery page preserves all seven source headings',all(soup.find(id='gallery-title-'+g['id']).get_text()==g['title'] for g in G))
for g in G:
 a=soup.select_one('[data-original-gallery='+g['id']+']')
 check('Gallery source link '+g['id'],a and a['href']==g['url'] and a.get('target')=='_blank' and {'noopener','noreferrer'}.issubset(set(a['rel'])))
for p in [R/'index.html',*list((R/'services').rglob('index.html')), *list((R/'blog').rglob('index.html')),R/'contact/index.html',R/'gallery/index.html']:
 h=BeautifulSoup(p.read_text(),'html.parser')
 check('Desktop/mobile/footer gallery route '+str(p.relative_to(R)),len(h.select('a[data-route="/gallery/"]'))>=3)
async def main():
 async with async_playwright() as pw:
  b=await pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  # Small portrait, compact landscape, tablet, both sides of the nav breakpoint, and widescreen.
  sizes=[(320,740),(360,800),(390,844),(430,932),(568,320),(844,390),(768,1024),(950,900),(1024,768),(1100,900),(1101,900),(1440,900),(1920,1080)]
  if os.getenv('R4_CASES'): sizes=[tuple(map(int,x.split('x'))) for x in os.getenv('R4_CASES').split(',')]
  for w,h in sizes:
   p=await b.new_page(viewport={'width':w,'height':h},reduced_motion='reduce');p.set_default_timeout(3500)
   errors=[];p.on('pageerror',lambda e,a=errors:a.append(str(e)))
   await p.set_content((R/'OPEN_PREVIEW.html').read_text(),wait_until='load');await images(p)
   tag=f'{w}x{h}'
   check('Hero content within frame '+tag,await p.evaluate('''()=>{const hero=document.querySelector('.hero').getBoundingClientRect();const nav=document.querySelector('.nav-wrap').getBoundingClientRect();return [...document.querySelectorAll('.hero h1,.hero-lead,.hero-buttons,.hero-region,.hero-bottom')].every(e=>{const r=e.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth+1&&r.top>=nav.bottom&&r.bottom<=hero.bottom+1})}'''))
   check('Hero rain respects reduced motion '+tag,await p.locator('.hero-rain').evaluate('e=>getComputedStyle(e).display==="none"||Number(getComputedStyle(e).opacity)===0'))
   check('Homepage has four compact real-project links '+tag,await p.locator('.project-mini[data-original-gallery]').count()==4 and await p.locator('.project-mini img').evaluate_all('is=>is.every(i=>i.getBoundingClientRect().width<=84&&i.naturalWidth===176)'))
   await go(p,'/gallery/');await images(p)
   dim=await bounds(p);check('Gallery has no horizontal overflow '+tag,dim['doc']<=w+1 and dim['body']<=w+1,dim)
   check('All gallery cards remain small and within frame '+tag,await p.locator('.gallery-card').evaluate_all('cs=>cs.every(c=>{const r=c.getBoundingClientRect();const im=c.querySelector("img");return r.left>=0&&r.right<=innerWidth+1&&im.getBoundingClientRect().width<=124&&im.naturalWidth===176})'))
   check('Seven gallery buttons at every size '+tag,await p.locator('.gallery-card-link').count()==7)
   if w<=1100:
    await p.locator('[data-mobile]').click()
    check('Mobile gallery menu opens '+tag,await p.locator('#mobile-menu').evaluate('d=>d.open') and await p.locator('[data-mobile]').get_attribute('aria-expanded')=='true')
    check('Navigation dialog fits viewport '+tag,await p.locator('#mobile-menu').evaluate('d=>{const r=d.getBoundingClientRect();return r.left>=0&&r.right<=innerWidth+1&&r.top>=0&&r.bottom<=innerHeight+1&&d.scrollWidth<=d.clientWidth+1}'))
    await p.locator('#mobile-menu a[data-route="/gallery/"]').click()
    check('Mobile Gallery route closes menu and unlocks body '+tag,await p.locator('#mobile-menu').evaluate('d=>!d.open') and await p.locator('body').evaluate('e=>!e.classList.contains("locked")'))
    check('Gallery current-page indicator in mobile menu '+tag,await p.locator('#mobile-menu a[data-route="/gallery/"]').get_attribute('aria-current')=='page')
    await p.locator('[data-mobile]').click();await p.locator('#mobile-menu details').evaluate('e=>e.open=true')
    await p.locator('#mobile-menu a[data-route="/services/wet-area-waterproofing/"]').click()
   else:
    await p.locator('.desktop-nav a[data-route="/gallery/"]').click()
    check('Desktop Gallery tab highlighted '+tag,await p.locator('.gallery-nav').get_attribute('aria-current')=='page')
    check('Desktop nav fits horizontally '+tag,await p.locator('.desktop-nav').evaluate('d=>{const r=d.getBoundingClientRect();return r.right<=innerWidth&&r.left>document.querySelector(".nav-wrap .brand").getBoundingClientRect().right}'))
    await go(p,'/services/wet-area-waterproofing/')
   check('Matching service album link '+tag,await p.locator('.service-projects [data-original-gallery]').get_attribute('href')==next(g['url'] for g in G if g['id']=='wetareas'))
   check('Service-project row stays in frame '+tag,(await bounds(p))['doc']<=w+1)
   await go(p,'/gallery/')
   if w<=1100:await p.locator('[data-mobile]').click()
   await p.locator('[data-search]:visible').first.click();await p.locator('#site-search').fill('gallery')
   check('Gallery searchable '+tag,await p.locator('.search-results a[data-route="/gallery/"]').count()==1)
   await p.locator('.search-results a[data-route="/gallery/"]').click()
   check('Gallery search result route '+tag,await p.locator('main[data-page=gallery]').count()==1)
   check('R4 gallery navigation has no uncaught exceptions '+tag,not errors,errors)
   await p.close()
  if os.getenv('R4_SKIP_EXTRA')=='1':
   await b.close();return
  # Exact external new-tab navigation tested with a local intercepted response, not remote album content.
  ctx=await b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce')
  await ctx.route('https://abraham311.editorx.io/**',lambda rt:rt.fulfill(status=200,content_type='text/html',body='<title>Intercepted navigation test</title>'))
  p=await ctx.new_page();await p.set_content((R/'OPEN_PREVIEW.html').read_text(),wait_until='load');await go(p,'/gallery/')
  for g in G:
   async with p.expect_popup() as popup:await p.locator('.gallery-card [data-original-gallery='+g['id']+']').click()
   tab=await popup.value;await tab.wait_for_load_state()
   check('Mapped album link creates isolated new tab '+g['id'],await p.locator('.gallery-card [data-original-gallery='+g['id']+']').get_attribute('href')==g['url'] and await tab.evaluate('window.opener===null'),{'source_href':g['url'],'browser_url':tab.url,'test':'Original href and a new isolated tab verified. Browser blocked URL loading; remote album rendering NOT verified.'})
   await tab.close()
  await ctx.close()
  # Visible, normal motion. Check that rain advances, manual pause stops it and offscreen work suspends.
  p=await b.new_page(viewport={'width':1440,'height':1000},reduced_motion='no-preference');p.set_default_timeout(4000)
  await p.set_content((R/'OPEN_PREVIEW.html').read_text(),wait_until='load');await images(p);await p.wait_for_timeout(1150)
  check('Normal hero motion enabled',await p.evaluate('document.documentElement.dataset.motion==="on"&&document.querySelector(".hero").dataset.effects==="active"'))
  running=await p.locator('.hero-rain i').first.evaluate('e=>e.getAnimations()[0]?.currentTime');await p.wait_for_timeout(170)
  check('Rain animation advances across hero',await p.locator('.hero-rain i').first.evaluate('e=>e.getAnimations()[0]?.currentTime')>running)
  await p.screenshot(path=str(V/'hero-rain-desktop.png'))
  await p.locator('button[data-motion]').evaluate('e=>e.click()')
  check('Footer motion control stops decorative rain',await p.evaluate('document.documentElement.dataset.motion==="off"&&document.querySelector(".hero").dataset.effects==="paused"'))
  await p.locator('button[data-motion]').evaluate('e=>e.click()');await p.wait_for_timeout(100)
  check('Footer motion control resumes hero effects',await p.locator('.hero').get_attribute('data-effects')=='active')
  await p.locator('[data-hero=cutaway]').click();await p.wait_for_timeout(1100)
  check('Alternate hero scene with readable heading',await p.locator('.hero-alt-photo').evaluate('e=>Number(getComputedStyle(e).opacity)>0.99') and await p.locator('h1').evaluate('e=>getComputedStyle(e).color==="rgb(255, 255, 255)"'))
  await p.screenshot(path=str(V/'hero-cutaway-desktop.png'))
  await p.locator('.project-proof').scroll_into_view_if_needed();await p.wait_for_timeout(120)
  check('Hero effects pause when scrolled offscreen',await p.locator('.hero').get_attribute('data-effects')=='paused')
  await p.evaluate('scrollTo({top:0,behavior:"instant"})');await p.wait_for_timeout(150)
  check('Hero effects resume on return to top',await p.locator('.hero').get_attribute('data-effects')=='active')
  await p.locator('button[data-motion]').evaluate('e=>e.click()');await go(p,'/gallery/');await go(p,'/')
  check('Navigation retains user motion preference',await p.evaluate('document.documentElement.dataset.motion==="off"&&document.querySelector("button[data-motion]").getAttribute("aria-pressed")==="false"'))
  await p.close();await b.close()
asyncio.run(main())
print('TOTAL',len(out),'PASS',sum(x['passed'] for x in out),'FAIL',sum(not x['passed'] for x in out))
raise SystemExit(0 if all(x['passed'] for x in out) else 1)
