#!/usr/bin/env python3
"""Repeatable structural and browser review. Uses inline assets; no deployment is implied."""
import asyncio,json,re,os,sys,subprocess,time,urllib.parse,shutil
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1];V=R/'verification';V.mkdir(exist_ok=True)
checks=[]
def check(name,ok,details=None):
 checks.append({'check':name,'passed':bool(ok),'details':details});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 (V/('checks-'+os.getenv('TEST_GROUP','all')+'.json')).write_text(json.dumps(checks,indent=2))
async def click_route(p,route):
 await p.evaluate("r=>{const a=document.createElement('a');a.dataset.route=r;a.href='#';document.body.append(a);a.click();a.remove();}",route)
 await p.wait_for_timeout(65)
async def images(p):
 await p.locator('img').evaluate_all('(ims)=>ims.forEach(i=>i.loading="eager")')
 await p.evaluate('Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))')
 return await p.evaluate('Array.from(document.images).filter(i=>!i.complete||!i.naturalWidth).map(i=>i.alt)')
async def dimensions(p):return await p.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth,body:document.body.scrollWidth})')
def static():
 paths=[R/'index.html',R/'404.html',*list((R/'services').rglob('index.html')),*list((R/'blog').rglob('index.html')),R/'contact/index.html',R/'gallery/index.html']
 titles=[];descs=[]
 for path in paths:
  soup=BeautifulSoup(path.read_text(),'html.parser');bad=[]
  for el in soup.select('[href],[src]'):
   val=el.get('href') or el.get('src');u=urllib.parse.urlsplit(val)
   if u.scheme or not u.path:continue
   target=(path.parent/urllib.parse.unquote(u.path)).resolve()
   if not target.exists():bad.append(val)
   elif u.fragment and target.suffix=='.html' and not BeautifulSoup(target.read_text(),'html.parser').find(id=urllib.parse.unquote(u.fragment)):bad.append('anchor:'+val)
  check('Local links and assets '+str(path.relative_to(R)),not bad,bad)
  if path.name!='404.html':
   titles.append(soup.title.text);descs.append(soup.select_one('meta[name=description]')['content'])
   check('Semantic page and preview SEO '+str(path.relative_to(R)),len(soup.select('h1'))==1 and bool(soup.select_one('main')) and 'noindex' in soup.select_one('meta[name=robots]')['content'])
   for s in soup.select('script[type="application/ld+json"]'):json.loads(s.string)
 check('All 18 page titles and descriptions unique',len(titles)==18 and len(set(titles))==18 and len(set(descs))==18)
 arts=json.loads((R/'content/articles.json').read_text());check('Eight full sourced guides',len(arts)==8 and all(x['words']>650 and len(x['sources'])>=3 for x in arts),{'words':sum(x['words'] for x in arts),'count':len(arts)})
 for script in ['app.js','house3d.js']:
  p=subprocess.run(['node','--check',str(R/'assets'/script)],capture_output=True,text=True);check('JavaScript parses '+script,p.returncode==0,p.stderr or None)
 check('No bundled fonts or secrets',not any(p.suffix.lower() in {'.woff','.woff2','.ttf','.otf','.eot','.pem','.key'} or p.name.startswith('.env') for p in R.rglob('*')))
 check('No false review ratings or prototype marketing copy in pages',not any(t in (R/'index.html').read_text().lower() for t in ['eight seo-rich','desktop + mobile optimized','premium review','5-star','10,000+']))
async def browser():
 group=os.getenv('TEST_GROUP','all');widths=[int(x) for x in os.getenv('WIDTHS','390,1440').split(',')]
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
  for width in widths:
   p=await browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1,reduced_motion='reduce')
   p.set_default_timeout(3500);errs=[];requests=[]
   p.on('pageerror',lambda e,a=errs:a.append(str(e)))
   p.on('request',lambda r,a=requests:a.append(r.url) if r.url.startswith(('http:','https:')) else None)
   await p.set_content((R/'OPEN_PREVIEW.html').read_text(),wait_until='load',timeout=20000)
   check(f'Homepage images {width}',not await images(p))
   d=await dimensions(p);check(f'Homepage horizontal layout {width}',d['scroll']<=width+1 and d['body']<=width+1,d)
   if width in (390,1440):
    await p.screenshot(path=str(V/f'homepage-{width}.png'),full_page=True)
    await p.screenshot(path=str(V/f'hero-{width}.png'))
   await p.locator('[data-hero]').last.click()
   # Use precise implemented keys rather than assume design copy.
   heroBtns=await p.locator('[data-hero]').evaluate_all('bs=>bs.map(b=>({key:b.dataset.hero,on:b.getAttribute("aria-pressed")}))')
   check(f'Hero scene toggle {width}',heroBtns[-1]['on']=='true',heroBtns)
   for i in range(5):
    await p.locator(f'.detail-stage [data-zone="{i}"]').click()
    check(f'Photo hotspot {width}/{i}',await p.locator(f'#zone-{i}').get_attribute('aria-selected')=='true')
   await p.locator('#zone-4').focus();await p.keyboard.press('Home');await p.keyboard.press('ArrowRight')
   check(f'Explorer keyboard {width}',await p.evaluate('document.activeElement.id')=='zone-1')
   if width in (390,1440):await p.locator('.explorer-shell').screenshot(path=str(V/f'cutaway-{width}.png'))
   if group!='layouts':
    await p.locator('[data-view=model]').click();await p.wait_for_timeout(120)
    metrics=await p.evaluate('(()=>{const m=W360_DEBUG.getModel();return m?{renderer:m.renderer,vertices:m.count,mode:m.mode,yaw:m.yaw,distance:m.distance}:null})()')
    check(f'Real 3D model initialized {width}',metrics and metrics['vertices']==15300,metrics)
    if metrics:
     y=metrics['yaw'];await p.locator('[data-rotate="1"]').click();await p.wait_for_timeout(100)
     check(f'3D rotation changes camera {width}',await p.evaluate('W360_DEBUG.getModel().yaw')!=y)
     await p.locator('[data-zoom="1"]').click();check(f'3D zoom changes perspective {width}',await p.evaluate('W360_DEBUG.getModel().distance')<metrics['distance'])
     for mode in ['exterior','exploded','cutaway']:
      await p.locator('[data-mode="'+mode+'"]').click();await p.wait_for_timeout(90)
      check(f'3D {mode} mode {width}',await p.evaluate('W360_DEBUG.getModel().mode')==mode)
      if mode=='exploded' and width in (390,1440):await p.locator('.explorer-shell').screenshot(path=str(V/f'model-exploded-{width}.png'))
     await p.locator('[data-reset]').click();await p.wait_for_timeout(50)
     if width in (390,1440):await p.locator('.explorer-shell').screenshot(path=str(V/f'model-{width}.png'))
     check(f'Reduced-motion model {width}',await p.evaluate('W360_DEBUG.getModel().motion')==False)
     await p.locator('[data-expand]').click();check(f'Expanded model opens {width}',await p.locator('.explorer-shell').get_attribute('aria-modal')=='true')
     await p.keyboard.press('Escape');check(f'Expanded model closes {width}',not await p.locator('.explorer-shell').evaluate('e=>e.classList.contains("expanded")'))
   await p.locator('[data-audience=builder]').click();check(f'Builder pathway {width}',await p.locator('.audience-cta').get_attribute('data-preset')=='new')
   await p.locator('[data-audience=specialty]').click();check(f'Specialty pathway {width}',await p.locator('.audience-cta').get_attribute('data-preset')=='wet')
   # Guide complete, no selection advances until an explicit choice.
   await p.locator('.hero [data-guide]').click();check(f'Guide requires choice {width}',await p.locator('[data-next]').is_disabled())
   for val in ['basement','existing','other']:
    await p.locator(f'[data-answer="{val}"]').click();await p.locator('[data-next]').click()
   check(f'Guide out-of-area qualification {width}',await p.locator('.outside').is_visible())
   await p.locator('[data-copy-brief]').click();check(f'Guide copy fallback {width}',await p.locator('.guide-notes').is_visible())
   check(f'Guide generated brief content {width}','Nothing has been sent' in await p.locator('.guide-notes').input_value())
   await p.locator('#project-dialog [data-inquire]').click();check(f'Existing external inquiry link {width}',await p.locator('.contact-links a[target]').get_attribute('href')=='https://api.leadconnectorhq.com/widget/form/KcGGVobxnDFogo3biqFe')
   await p.keyboard.press('Escape');check(f'Guide closes without body lock {width}',not await p.locator('body').evaluate('e=>e.classList.contains("locked")'))
   if width<=1100:
    await p.locator('[data-mobile]').click();check(f'Mobile menu opens {width}',await p.locator('#mobile-menu').evaluate('d=>d.open'));await p.keyboard.press('Escape')
   else:
    await p.locator('[data-menu]').click();check(f'Desktop solution menu {width}',await p.locator('#solutions-menu').is_visible());await p.keyboard.press('Escape')
   # Navigate using the same route handler as clicks in the single-file review.
   await click_route(p,'/blog/');check(f'Journal all eight guides {width}',await p.locator('.all-guides .article-card:visible').count()==8)
   check(f'Journal images {width}',not await images(p));d=await dimensions(p);check(f'Journal layout {width}',d['scroll']<=width+1,d)
   if width in (390,1440):await p.screenshot(path=str(V/f'journal-{width}.png'),full_page=True)
   await p.locator('#journal-search').fill('condensation');check(f'Journal topic search {width}',await p.locator('.all-guides .article-card:visible').count()==1)
   await p.locator('#journal-search').fill('xyzqnotfound');check(f'Journal no-results state {width}',await p.locator('.no-results').is_visible());await p.locator('[data-reset-filters]').click();check(f'Journal reset {width}',await p.locator('.all-guides .article-card:visible').count()==8)
   await p.locator('[data-category-filter="Drainage"]').click();check(f'Journal category filter {width}',await p.locator('.all-guides .article-card:visible').count()==1)
   for a in json.loads((R/'content/articles.json').read_text()):
    await click_route(p,'/blog/'+a['slug']+'/');await images(p)
    check(f'Article route {width}/{a["slug"]}',await p.locator('h1').inner_text()==a['title'])
    d=await dimensions(p);check(f'Article layout {width}/{a["slug"]}',d['scroll']<=width+1,d)
   await click_route(p,'/blog/basement-water-after-rain/');await images(p)
   await p.locator('[data-toc]').first.click();check(f'Article TOC navigation {width}',await p.evaluate('scrollY')>0)
   for el in await p.locator('[data-checklist]').all():await el.check()
   check(f'Article preparation checklist {width}','4 of 4' in await p.locator('.check-status').inner_text())
   if width in (390,1440):await p.screenshot(path=str(V/f'article-{width}.png'),full_page=True)
   for s in json.loads((R/'content/services.json').read_text()):
    await click_route(p,'/services/'+s['slug']+'/');check(f'Service page {width}/{s["id"]}',await p.locator('main[data-page="service"]').count()==1)
    check(f'Service images and layout {width}/{s["id"]}',not await images(p) and (await dimensions(p))['scroll']<=width+1)
   await click_route(p,'/contact/');check(f'Contact page {width}',await p.locator('main[data-page=contact]').count()==1)
   if width<=1100:await p.locator('[data-mobile]').click()
   await p.locator('[data-search]:visible').first.click();await p.locator('#site-search').fill('drainage');check(f'Site-wide search {width}',await p.locator('.search-results a').count()>0);await p.locator('.search-results a').first.click();check(f'Search result navigation {width}',not await p.locator('#search-dialog').evaluate('d=>d.open'))
   check(f'No uncaught errors {width}',not errs,errs)
   check(f'No automatic external requests {width}',not requests,requests)
   await p.close()
  await browser.close()
if __name__=='__main__':
 if os.getenv('TEST_GROUP')=='static':static()
 else:asyncio.run(browser())
 print('TOTAL',len(checks),'PASS',sum(x['passed'] for x in checks),'FAIL',sum(not x['passed'] for x in checks))
 sys.exit(0 if all(x['passed'] for x in checks) else 1)
