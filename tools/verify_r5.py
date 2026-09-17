#!/usr/bin/env python3
"""Verify R5's exact logo, default motion, controls, responsive header, and baseline preservation.
Uses actual packaged preview in Chromium; no publication or external submission.
"""
import asyncio, json, hashlib, re, os
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1];V=R/'verification';rows=[]
def check(name,ok,detail=None):
 rows.append({'check':name,'passed':bool(ok),'details':detail});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 (V/'checks-r5.json').write_text(json.dumps(rows,indent=2))
async def images(p):
 return await p.evaluate('''async()=>{await Promise.all([...document.images].map(async i=>{i.loading='eager';try{await i.decode()}catch{}}));return [...document.images].filter(i=>!i.naturalWidth).map(i=>i.alt)}''')
async def go(p,route):
 await p.evaluate("r=>{const a=document.createElement('a');a.dataset.route=r;a.href='#';document.body.append(a);a.click();a.remove();}",route)
 await p.wait_for_timeout(80)
async def state(p):
 return await p.evaluate('''()=>{const m=W360_DEBUG.getModel();return m?{rain:m.rain,orbit:m.orbit,motion:m.motion,yaw:m.yaw,time:m.time,mode:m.mode,renderer:m.renderer,visible:m.visible,rainButton:document.querySelector('[data-rain]').getAttribute('aria-pressed'),orbitButton:document.querySelector('[data-orbit]').getAttribute('aria-pressed')}:null}''')
def on(s):return s and s['motion'] and s['rain'] and s['orbit'] and s['rainButton']=='true' and s['orbitButton']=='true'

def static():
 baseline=json.loads((V/'r4-baseline.json').read_text())
 check('Original supplied logo byte-for-byte',hashlib.sha256((R/'assets/logo.png').read_bytes()).hexdigest()==baseline['supplied_logo_sha256'])
 for x in baseline['unchanged']:
  check('R4 asset/content preserved: '+x['path'],hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256'])
 for r in json.loads((R/'content/route-manifest.json').read_text()):
  route=r['route'];p=R/route.strip('/')/'index.html' if route!='/' else R/'index.html'
  soup=BeautifulSoup(p.read_text(),'html.parser')
  logos=soup.select('.brand img.brand-logo')
  check('All brand placements use original PNG: '+route,len(logos)==3 and all(i['src'].endswith('assets/logo.png') and i.get('alt')=='Waterproofing360' for i in logos) and not soup.select('.brand svg'))
 check('Hero Pause effects control removed from source and preview',all('data-hero-motion' not in (R/n).read_text() for n in ['index.html','OPEN_PREVIEW.html','assets/app.js']))
 check('Homepage Rain and Orbit controls selected before JS initialization',all(BeautifulSoup((R/'index.html').read_text(),'html.parser').select_one(sel)['aria-pressed']=='true' for sel in ['[data-rain]','[data-orbit]']))
 check('Favicon reuses uploaded pixels rather than prior replacement artwork','data:image/png;base64,' in (R/'assets/favicon.svg').read_text())

async def main():
 async with async_playwright() as pw:
  b=await pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  for w,h in [(320,740),(390,844),(568,320),(768,1024),(1100,900),(1101,900),(1440,900),(1920,1080)]:
   p=await b.new_page(viewport={'width':w,'height':h},reduced_motion='no-preference');p.set_default_timeout(6000);errs=[]
   p.on('pageerror',lambda e,a=errs:a.append(str(e)))
   await p.set_content((R/'OPEN_PREVIEW.html').read_text(),wait_until='load');await images(p);await p.wait_for_timeout(1000)
   dim=await p.evaluate('''()=>{const brand=document.querySelector('.nav-wrap .brand').getBoundingClientRect();const logo=document.querySelector('.nav-wrap .brand-logo');const lr=logo.getBoundingClientRect();const nav=document.querySelector('.nav-wrap').getBoundingClientRect();const controls=document.querySelector(innerWidth<=1100?'[data-mobile]':'.desktop-nav').getBoundingClientRect();return {w:innerWidth,sw:document.documentElement.scrollWidth,logoW:lr.width,logoH:lr.height,naturalW:logo.naturalWidth,naturalH:logo.naturalHeight,brandRight:brand.right,controlsLeft:controls.left,navBottom:nav.bottom,within:brand.left>=nav.left&&brand.right<=nav.right&&brand.bottom<=nav.bottom}}''')
   check(f'Exact logo fits responsive header {w}x{h}',dim['naturalW']==300 and dim['naturalH']==90 and abs(dim['logoW']/dim['logoH']-300/90)<.01 and dim['logoW']<=300 and dim['sw']<=w+1 and dim['within'] and dim['brandRight']<dim['controlsLeft'],dim)
   check(f'Hero effects on without hero pause button {w}',await p.evaluate('document.documentElement.dataset.motion==="on"&&document.querySelector(".hero").dataset.effects==="active"&&!document.querySelector("[data-hero-motion]")'))
   if w in [390,1440]:await p.screenshot(path=str(V/f'r5-hero-{w}.png'))
   if w<=1100:
    await p.locator('[data-mobile]').click();await images(p)
    check(f'Mobile logo and menu remain in frame {w}',await p.locator('#mobile-menu').evaluate('''d=>{const r=d.getBoundingClientRect(),i=d.querySelector('.brand-logo').getBoundingClientRect(),close=d.querySelector('[data-close]').getBoundingClientRect();return d.open&&r.left>=0&&r.right<=innerWidth+1&&r.top>=0&&r.bottom<=innerHeight+1&&d.scrollWidth<=d.clientWidth+1&&i.right<=close.left}'''))
    if w==390:await p.screenshot(path=str(V/'r5-mobile-menu.png'))
    await p.keyboard.press('Escape')
   else:
    await p.locator('[data-menu]').click();check(f'Desktop solutions menu works {w}',await p.locator('#solutions-menu').is_visible());await p.keyboard.press('Escape')
   if w not in [390,1440]:await p.close();continue
   await p.locator('[data-view=model]').click();await p.wait_for_timeout(300)
   s=await state(p);check(f'Live 3D starts raining and orbiting {w}',on(s),s)
   await p.wait_for_timeout(250);t=await state(p);check(f'Rain timeline and camera advance by default {w}',t['time']>s['time'] and t['yaw']>s['yaw'],{'before':s,'after':t})
   await p.locator('.explorer-shell').screenshot(path=str(V/f'r5-live3d-{w}.png'),timeout=15000)
   await p.locator('[data-rain]').click();s=await state(p);check(f'Rain toggle turns off only rain {w}',not s['rain'] and s['orbit'] and s['rainButton']=='false')
   await p.locator('[data-rain]').click();await p.locator('[data-orbit]').click();s=await state(p);check(f'Orbit toggle turns off only orbit {w}',s['rain'] and not s['orbit'] and s['orbitButton']=='false')
   await p.locator('[data-reset]').click();s=await state(p);check(f'Reset restores both enabled defaults {w}',on(s) and s['mode']=='cutaway',s)
   await p.locator('[data-rotate="1"]').click();s=await state(p);check(f'Manual camera control pauses orbit and retains rain {w}',not s['orbit'] and s['rain'] and s['orbitButton']=='false')
   await p.locator('#house-canvas').focus();await p.keyboard.press('Home');s=await state(p);check(f'Keyboard Home restores both defaults {w}',on(s),s)
   await p.locator('#house-canvas').focus();await p.keyboard.press('ArrowLeft');s=await state(p);check(f'Keyboard rotation synchronizes Orbit selection {w}',not s['orbit'] and s['orbitButton']=='false' and s['rain'])
   await p.locator('[data-reset]').click();await p.locator('[data-view=detail]').click();check(f'Detailed view suspends live renderer {w}',not (await state(p))['visible'])
   await p.locator('[data-view=model]').click();check(f'Reopening Live 3D retains enabled effects {w}',on(await state(p)))
   await go(p,'/gallery/');await images(p);check(f'Gallery still has seven distinct albums {w}',await p.locator('.gallery-card [data-original-gallery]').count()==7)
   await go(p,'/');await p.locator('[data-view=model]').click();check(f'Returning home reinitializes Live 3D defaults {w}',on(await state(p)))
   await p.locator('button[data-motion]').evaluate('e=>e.click()');s=await state(p);check(f'Footer accessibility setting stops effects {w}',not s['motion'] and not s['rain'] and not s['orbit'] and s['rainButton']=='false' and s['orbitButton']=='false')
   await p.locator('button[data-motion]').evaluate('e=>e.click()');check(f'Footer re-enable restores default motion {w}',on(await state(p)))
   await p.locator('[data-view=detail]').click();await p.locator('.site-header .brand').click();await images(p);await p.wait_for_timeout(100)
   check(f'Header logo returns home {w}',await p.evaluate('W360_DEBUG.getRoute()==="/"'))
   await p.locator('footer .brand').scroll_into_view_if_needed();check(f'Footer original logo readable at native aspect {w}',await p.locator('footer .brand-logo').evaluate('e=>e.naturalWidth===300&&e.getBoundingClientRect().width<=300&&getComputedStyle(e).filter==="none"'))
   if w==1440:await p.locator('footer').screenshot(path=str(V/'r5-footer.png'))
   check(f'No uncaught exceptions {w}',not errs,errs)
   await p.close()
  # OS motion preference wins, including when changed during a session.
  p=await b.new_page(viewport={'width':390,'height':844},reduced_motion='reduce');p.set_default_timeout(6000)
  await p.set_content((R/'OPEN_PREVIEW.html').read_text(),wait_until='load');await images(p)
  check('Reduced motion disables hero animation automatically',await p.evaluate('document.documentElement.dataset.motion==="off"&&getComputedStyle(document.querySelector(".hero-rain")).display==="none"'))
  await p.locator('[data-view=model]').click();s=await state(p);check('Reduced motion disables live rain/orbit and unselects controls',s and not s['motion'] and not s['rain'] and not s['orbit'] and s['rainButton']=='false' and s['orbitButton']=='false',s)
  await p.locator('[data-reset]').click();s=await state(p);check('Reset respects reduced motion',not s['rain'] and not s['orbit'])
  await p.locator('button[data-motion]').evaluate('e=>e.click()');check('Deliberate footer Motion on permits animation',on(await state(p)))
  await p.emulate_media(reduced_motion='no-preference');await p.wait_for_timeout(180);await p.emulate_media(reduced_motion='reduce');await p.wait_for_timeout(100)
  s=await state(p);check('Live OS setting change stops all effects',not s['motion'] and not s['rain'] and not s['orbit'])
  await p.close();await b.close()
static();asyncio.run(main());print('TOTAL',len(rows),'PASS',sum(x['passed']for x in rows),'FAIL',sum(not x['passed']for x in rows));raise SystemExit(0 if all(x['passed']for x in rows) else 1)
