#!/usr/bin/env python3
"""Deeper interaction tests; records local browser evidence, not hosting success."""
import asyncio,json,time,re,sys
from pathlib import Path
from playwright.async_api import async_playwright
R=Path(__file__).resolve().parents[1];result=[]
def check(n,ok,d=None):
 result.append({'check':n,'passed':bool(ok),'details':d});print(('PASS 'if ok else 'FAIL ')+n,flush=True)
 (R/'verification/checks-advanced.json').write_text(json.dumps(result,indent=2))
async def main():
 async with async_playwright() as pw:
  b=await pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  p=await b.new_page(viewport={'width':1440,'height':900});p.set_default_timeout(4000);errs=[]
  p.on('pageerror',lambda e:errs.append(str(e)))
  await p.set_content((R/'OPEN_PREVIEW.html').read_text(),wait_until='load')
  await p.locator('[data-view=model]').click();await p.wait_for_timeout(100)
  await p.locator('[data-mode=exploded]').click();await p.wait_for_timeout(1100)
  m=await p.evaluate('(()=>{let m=W360_DEBUG.getModel();return {renderer:m.renderer,explode:m.explode,goal:m.targetExplode,yaw:m.yaw,distance:m.distance,vertices:m.count}})()')
  check('Animated exploded layers settle toward the target',abs(m['explode']-.6)<.02,m)
  await p.locator('.explorer-shell').screenshot(path=str(R/'verification/exploded-final.png'))
  await p.locator('[data-reset]').click();await p.wait_for_timeout(700)
  check('Reset restores cutaway, camera and enabled rain/orbit defaults',await p.evaluate('(()=>{const m=W360_DEBUG.getModel();return m.mode==="cutaway"&&m.distance===21&&m.yaw>=.61&&m.orbit&&m.rain})()'))
  box=await p.locator('#house-canvas').bounding_box();y=await p.evaluate('W360_DEBUG.getModel().yaw')
  await p.mouse.move(box['x']+box['width']*.55,box['y']+box['height']*.65);await p.mouse.down();await p.mouse.move(box['x']+box['width']*.55+85,box['y']+box['height']*.65,steps=8);await p.mouse.up()
  check('Pointer drag orbits the real model',abs(await p.evaluate('W360_DEBUG.getModel().yaw')-y)>.1)
  await p.locator('#house-canvas').focus();y=await p.evaluate('W360_DEBUG.getModel().yaw');await p.keyboard.press('ArrowLeft');check('Canvas keyboard rotates',await p.evaluate('W360_DEBUG.getModel().yaw')!=y)
  await p.locator('[data-rain]').click();check('Default rain can be switched off',not await p.evaluate('W360_DEBUG.getModel().rain'))
  await p.locator('[data-rain]').click();check('Rain can be re-enabled',await p.evaluate('W360_DEBUG.getModel().rain'))
  t=await p.evaluate('W360_DEBUG.getModel().time');await p.wait_for_timeout(200);check('Rain animation advances',await p.evaluate('W360_DEBUG.getModel().time')>t)
  await p.locator('[data-orbit]').click();y=await p.evaluate('W360_DEBUG.getModel().yaw');await p.wait_for_timeout(300);check('Re-enabled auto orbit changes camera',await p.evaluate('W360_DEBUG.getModel().yaw')!=y)
  await p.locator('[data-rotate="1"]').click();check('Manual rotation cancels auto orbit',not await p.evaluate('W360_DEBUG.getModel().orbit') and await p.locator('[data-orbit]').get_attribute('aria-pressed')=='false')
  await p.locator('button[data-motion]').click();check('Global motion setting stops animation',await p.evaluate('document.documentElement.dataset.motion==="off"&&!W360_DEBUG.getModel().rain&&!W360_DEBUG.getModel().orbit&&!W360_DEBUG.getModel().motion'))
  await p.locator('[data-rain]').click();check('Reduced motion prevents optional animated rain',not await p.evaluate('W360_DEBUG.getModel().rain'))
  await p.locator('[data-expand]').click();focusable=p.locator('.explorer-shell button:visible,.explorer-shell a:visible,.explorer-shell canvas:visible')
  await focusable.last.focus();await p.keyboard.press('Tab');check('Expanded model traps forward focus',await p.evaluate('document.activeElement===document.querySelector(".explorer-toolbar [data-view]")'))
  await p.keyboard.press('Escape');check('Expanded model releases lock',await p.evaluate('!document.body.classList.contains("locked")'))
  await p.locator('[data-view=detail]').click();check('Image view pauses 3D rendering',not await p.evaluate('W360_DEBUG.getModel().visible'))
  await p.locator('[data-view=model]').click();await p.wait_for_timeout(50)
  frame=await p.evaluate('(()=>{const m=W360_DEBUG.getModel();const t=performance.now();m.render(t);return performance.now()-t})()');check('3D render completes',frame<500,{'milliseconds_single_frame':round(frame,2),'renderer':m['renderer'],'not_a_cross_device_FPS_benchmark':True})
  await p.evaluate('window.__priorModel=W360_DEBUG.getModel();document.querySelector(".zone-link").click()');await p.wait_for_timeout(60)
  check('Leaving the house disposes renderer resources',await p.evaluate('window.__priorModel.dead&&W360_DEBUG.getModel()===null'))
  await p.keyboard.press('Control+k');check('Site search keyboard shortcut',await p.locator('#search-dialog').evaluate('d=>d.open'));await p.keyboard.press('Escape')
  # Trigger known preset then verify navigation/back and a generated download event.
  await p.locator('main [data-guide]').first.click();check('Service CTA carries a preset',await p.locator('[data-answer=existing]').count()==1)
  await p.locator('[data-answer=existing]').click();await p.locator('[data-next]').click();await p.locator('[data-answer=ny]').click();await p.locator('[data-next]').click()
  check('In-area result is qualified without an outside-area warning',await p.locator('.outside').count()==0 and 'not' in (await p.locator('.guide-privacy').inner_text()).lower())
  async with p.expect_download(timeout=4000) as dl:await p.locator('[data-download-brief]').click()
  download=await dl.value;check('Actual project brief download event',download.suggested_filename=='Waterproofing360-project-brief.txt')
  await p.locator('[data-back]').click();check('Guide back retains previous answer',await p.locator('[data-answer=ny]').get_attribute('aria-pressed')=='true')
  await p.keyboard.press('Escape')
  # Fallback when both canvas engines unavailable is still a working photo explorer.
  await p.evaluate('document.querySelector(".brand[data-route]").click()');await p.wait_for_timeout(60)
  await p.evaluate('(()=>{window.W360House=class {constructor(){throw Error("Simulated no canvas graphics")}};return true;})()')
  await p.locator('[data-view=model]').click();check('No-graphics fallback preserves accessible detailed view',await p.locator('.detail-stage').is_visible() and await p.locator('[data-view=detail]').get_attribute('aria-pressed')=='true')
  await p.locator('#zone-3').click();check('Fallback retains all service-zone controls',await p.locator('#zone-3').get_attribute('aria-selected')=='true')
  check('Advanced interactions have no uncaught exceptions',not errs,errs)
  await b.close()
asyncio.run(main());print('TOTAL',len(result),'PASS',sum(x['passed']for x in result),'FAIL',sum(not x['passed']for x in result));sys.exit(not all(x['passed'] for x in result))
