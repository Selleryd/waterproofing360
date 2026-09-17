/* Waterproofing360 R5: no analytics, cookies, remote scripts, or automatic form submissions. */
(() => {
'use strict';
const data = JSON.parse(document.getElementById('site-data').textContent);
const pages = window.W360_PAGES || null;
const media = window.W360_MEDIA || {};
const $ = (s,scope=document) => scope.querySelector(s);
const $$ = (s,scope=document) => Array.from(scope.querySelectorAll(s));
const esc = s => String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const arrow='<span aria-hidden="true">↗</span>';
let activeRoute=window.W360_ROUTE || document.body.dataset.route || '/', zone=0, model=null, modelVisible=false;
let heroEffectsObserver=null, heroOnscreen=true;
let animationOn=!matchMedia('(prefers-reduced-motion: reduce)').matches;
let guide={step:0,answers:[null,null,null]}, lastFocus=null, toastTimer=null;
let expanded=false, expandedFocus=null, journalCategory='All', sceneObserver=null;
const dialog=$('#project-dialog'), dialogBody=$('#dialog-body'), mobile=$('#mobile-menu'), searchDialog=$('#search-dialog');
const steps=[
 {title:'What brings you here?',hint:'Choose the closest starting point. You do not need to know the cause.',items:[['basement','Water in the basement'],['crack','A visible crack'],['drainage','A drainage concern'],['new','A new project'],['wet','A shower, spa, or pool'],['unsure','I’m not sure yet']]},
 {title:'Where is the project now?',hint:'A little context helps frame a more useful conversation.',items:[['existing','An existing concern'],['renovation','A renovation'],['construction','New construction'],['planning','Early planning']]},
 {title:'Where is the property?',hint:'The team will confirm coverage and availability for your specific location.',items:[['ny','New York'],['nj','New Jersey'],['other','Somewhere else']]}
];
const audiences={
 homeowner:{i:0,kicker:'For the home you live in',title:'You know the home.<br>Let’s understand the concern.',text:'Bring what you’ve noticed: the wet corner, the timing, the previous repair. You do not need to know the cause to start a useful conversation.',cta:'Tell us what you’re noticing',preset:'',items:['Existing leaks and recurring moisture','Drainage questions around the property','Planning before you finish a basement']},
 builder:{i:1,kicker:'For the details still taking shape',title:'Bring the plans.<br>Keep the layers connected.',text:'Coordinate waterproofing while access, penetrations, and the construction sequence can still be considered together. Start with the current drawings and the next milestone.',cta:'Discuss a planned project',preset:'new',items:['Below-grade concrete foundation details','Underslab protection and penetrations','Trade coordination before concealment']},
 specialty:{i:2,kicker:'For spaces with different demands',title:'Beautiful finishes.<br>A considered assembly.',text:'Showers, spas, mikvahs, and pools each need a conversation around actual use, exposure, and the details underneath. Bring the vision and the construction context.',cta:'Discuss your specialty space',preset:'wet',items:['Shower and wet-room assemblies','Spa, mikvah, and pool contexts','Connections, testing, and documentation']}
};
function notify(text){const n=$('#toast');n.textContent=text;n.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>n.hidden=true,4500);}
function syncLock(){document.body.classList.toggle('locked',expanded || $$('dialog[open]').length>0);}
function closeMenus(){const menu=$('#solutions-menu');if(menu)menu.hidden=true;const b=$('[data-menu]');if(b)b.setAttribute('aria-expanded','false');}
function closeDialogs(){for(const d of $$('dialog[open]'))d.close();syncLock();}
function openDialog(d){closeMenus();lastFocus=document.activeElement;for(const old of $$('dialog[open]'))if(old!==d)old.close();if(!d.open)d.showModal();syncLock();requestAnimationFrame(()=>{const t=d===searchDialog?$('#site-search'):d===mobile?$('.mobile-links a',d):$('#dialog-title');if(t){t.tabIndex=t.tagName==='H2'?-1:t.tabIndex;t.focus({preventScroll:true});}});}
for(const d of $$('dialog')){
 d.addEventListener('cancel',e=>{e.preventDefault();d.close();syncLock();});
 d.addEventListener('close',()=>{syncLock();$('[data-mobile]').setAttribute('aria-expanded','false');if(lastFocus&&lastFocus.isConnected&&!$('dialog[open]'))lastFocus.focus({preventScroll:true});});
 d.addEventListener('click',e=>{if(e.target!==d)return;const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();});
}
function guideStart(preset=''){
 const valid=steps[0].items.some(x=>x[0]===preset);
 guide={step:valid?1:0,answers:[valid?preset:null,null,null]};renderGuide();openDialog(dialog);
}
function titleFocus(){const el=$('#dialog-title');if(el){el.tabIndex=-1;el.focus({preventScroll:true});}dialog.scrollTop=0;}
function renderGuide(){
 if(guide.step===3){renderResult();return;}
 const s=steps[guide.step];
 dialogBody.innerHTML=`<p class="kicker">Your property guide / Step ${guide.step+1} of 3</p><div class="guide-progress" aria-hidden="true">${steps.map((_,i)=>`<i class="${i<=guide.step?'on':''}"></i>`).join('')}</div><h2 id="dialog-title">${s.title}</h2><p class="dialog-dek">${s.hint}</p><div class="guide-options" role="group" aria-label="${s.title}">${s.items.map(([v,t])=>`<button type="button" class="guide-option" data-answer="${v}" aria-pressed="${guide.answers[guide.step]===v}">${t}</button>`).join('')}</div><p class="guide-privacy">No name, email, phone number, or address is collected in this guide. Your choices stay in this page.</p><div class="guide-nav"><button type="button" class="plain" data-back>← ${guide.step?'Back':'Close'}</button><button type="button" class="btn compact" data-next ${guide.answers[guide.step]?'':'disabled'}>Continue ${arrow}</button></div>`;
 if(dialog.open)titleFocus();
}
const label=(i,v)=>steps[i].items.find(x=>x[0]===v)?.[1]||'';
function selectedService(){const m={basement:'foundation',crack:'cracks',drainage:'drainage',new:'concrete',wet:'wetareas',unsure:'foundation'};return data.services.find(s=>s.id===m[guide.answers[0]])||data.services[0];}
function brief(){const s=selectedService();return 'WATERPROOFING360 — PROJECT CONVERSATION BRIEF\n\n'+guide.answers.map((v,i)=>steps[i].title+'\n'+label(i,v)).join('\n\n')+'\n\nTopic to discuss: '+(guide.answers[0]==='unsure'?'Start with what you have observed':s.name)+'\n'+(guide.answers[2]==='other'?'Coverage must be confirmed; property is outside the currently stated NY/NJ service area.\n':'')+'\nBEFORE THE CONVERSATION\n- Note where and when the concern appears.\n- Gather photographs taken safely.\n- Find available plans and previous repair records.\n- Write down questions about scope, access, restoration, and maintenance.\n\nContact: (845) 388-1443\n\nThis guide is not a diagnosis, specification, quote, booking, or coverage confirmation. Nothing has been sent to the company.\n';}
function renderResult(){
 const s=selectedService();const unsure=guide.answers[0]==='unsure';
 dialogBody.innerHTML=`<p class="kicker">Your property guide / A clearer starting point</p><h2 id="dialog-title">Bring the details.<br>Start the conversation.</h2><p class="dialog-dek">Here is a short brief you can keep or share directly with the team.</p><div class="guide-result"><div class="guide-chips">${guide.answers.map((v,i)=>`<span>${esc(label(i,v))}</span>`).join('')}</div><h3>${unsure?'Start with what you have observed.':esc(s.name)}</h3><p>${unsure?'You do not need to choose a service. Explain where the concern appears and what you want to do with the space.':esc(s.summary)}</p>${guide.answers[2]==='other'?'<p class="outside">Please confirm coverage first. This location is outside the currently stated New York and New Jersey service area.</p>':''}</div><div class="guide-actions"><button type="button" class="btn compact" data-inquire>Contact the team ${arrow}</button><button type="button" class="plain" data-download-brief>Download brief ↓</button><button type="button" class="plain" data-copy-brief>Copy notes ↗</button></div><textarea class="guide-notes" aria-label="Project notes, select to copy" readonly hidden></textarea><p class="guide-privacy">A topic to discuss—not a diagnosis, quote, appointment, or system recommendation. These choices are not sent automatically.</p><div class="guide-nav"><button type="button" class="plain" data-back>← Back</button><button type="button" class="plain" data-guide>Start again ↗</button></div>`;if(dialog.open)titleFocus();
}
function contactPanel(){dialogBody.innerHTML=`<p class="kicker">Continue the conversation</p><h2 id="dialog-title">Let’s talk about<br>your property.</h2><p class="dialog-dek">Choose how you would like to get in touch.</p><div class="contact-links"><a href="tel:+18453881443"><b>(845) 388-1443 ${arrow}</b><span>Call Waterproofing360</span></a><a href="${esc(data.form)}" target="_blank" rel="noopener noreferrer"><b>Open the inquiry form ${arrow}</b><span>Opens the existing company provider in a new tab.</span></a></div><p class="guide-privacy">Nothing has been submitted. Guide selections are not transmitted automatically. Confirm location, scope, and availability with the team.</p><div class="guide-nav"><button type="button" class="plain" ${guide.step===3?'data-result':'data-close'}>← ${guide.step===3?'Back to your brief':'Close'}</button></div>`;openDialog(dialog);}
function saveText(text,filename){const u=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=u;a.download=filename;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),5000);}
async function copyText(text,fallback){try{if(!navigator.clipboard||!isSecureContext)throw Error('Clipboard unavailable');await navigator.clipboard.writeText(text);notify('Copied. Nothing was sent to the company.');}catch{if(fallback){fallback.value=text;fallback.hidden=false;fallback.focus();fallback.select();notify('Your browser requires manual copying. The notes are selected.');}else notify('Copy the page address from your browser’s address bar.');}}
function setZone(i,focus=false){
 if(!data.zones[i]||!$('.explorer-shell'))return;zone=i;const z=data.zones[i];
 $$('.zone-tab').forEach((b,n)=>{b.setAttribute('aria-selected',String(n===i));b.tabIndex=n===i?0:-1;if(n===i&&focus)b.focus({preventScroll:true});if(n===i&&innerWidth<=720){const parent=b.parentElement;parent.scrollTo({left:Math.max(0,b.offsetLeft-parent.offsetLeft-10),behavior:'instant'});}});
 $$('.hotspot').forEach(b=>b.setAttribute('aria-pressed',String(Number(b.dataset.zone)===i)));
 $('.zone-tag').textContent=z.tag;$('.zone-headline').textContent=z.headline;$('.zone-copy').textContent=z.text;$('#zone-detail').setAttribute('aria-labelledby','zone-'+i);
 const s=data.services.find(s=>s.id===z.service), l=$('.zone-link');l.dataset.route='/services/'+s.slug+'/';l.innerHTML='Explore '+esc(s.name.toLowerCase())+' '+arrow;l.href=pages?routeHash(l.dataset.route):relativeRoute(l.dataset.route);
 if(model)model.setZone(i);
}
function selectView(view){
 const live=view==='model';modelVisible=live;
 $$('.explorer-toolbar [data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
 $('.detail-stage').hidden=live;$('.live-stage').hidden=!live;$('.model-controls').hidden=!live;
 if(live&&!model){
  try{model=new window.W360House($('#house-canvas'),$('.model-pins'),i=>setZone(i));model.setMotion(animationOn);model.setRain(animationOn);model.setOrbit(animationOn);model.setZone(zone);setZone(zone);$('.model-status').textContent=(model.renderer==='webgl'?'LIVE 3D':'LIVE 3D · COMPATIBILITY MODE')+' / Drag to orbit';}
  catch(e){console.warn('3D unavailable:',e.message);$('.model-status').textContent='3D is not available in this browser. The detailed cutaway and all service tabs still work.';$('.model-controls').hidden=true;$('.detail-stage').hidden=false;$('.live-stage').hidden=true;modelVisible=false;$$('.explorer-toolbar [data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view==='detail')));notify('3D graphics are unavailable here. Showing the detailed cutaway instead.');return;}
 }
 if(model){model.setVisible(live);if(live)requestAnimationFrame(()=>model?.resize());}
}
function setAudience(key,focus=false){const a=audiences[key];if(!a||!$('#audience-panel'))return;$$('[data-audience]').forEach((b,i)=>{b.setAttribute('aria-selected',String(b.dataset.audience===key));b.tabIndex=b.dataset.audience===key?0:-1;if(b.dataset.audience===key&&focus)b.focus({preventScroll:true});});$('#audience-panel').setAttribute('aria-labelledby','audience-'+a.i);$('.audience-number').textContent='0'+(a.i+1);$('.audience-kicker').textContent=a.kicker;$('.audience-title').innerHTML=a.title;$('.audience-text').textContent=a.text;$('.audience-cta').innerHTML=a.cta+' '+arrow;$('.audience-cta').dataset.preset=a.preset;$('.audience-list').innerHTML=a.items.map(x=>'<li>'+esc(x)+'</li>').join('');}
function toggleExpanded(){
 const shell=$('.explorer-shell');if(!shell)return;
 expanded=!expanded;shell.classList.toggle('expanded',expanded);const b=$('[data-expand]');b.textContent=expanded?'×':'⤢';b.setAttribute('aria-label',expanded?'Close expanded house explorer':'Expand house explorer');
 if(expanded){expandedFocus=document.activeElement;shell.setAttribute('role','dialog');shell.setAttribute('aria-modal','true');shell.setAttribute('aria-label','Expanded house explorer');b.focus({preventScroll:true});}
 else{shell.removeAttribute('role');shell.removeAttribute('aria-modal');shell.removeAttribute('aria-label');if(expandedFocus?.isConnected)expandedFocus.focus({preventScroll:true});}
 syncLock();if(model)requestAnimationFrame(()=>model?.resize());
}
function syncHeroEffects(){
 const h=$('.hero');if(h)h.dataset.effects=animationOn&&!document.hidden&&heroOnscreen?'active':'paused';
}
function initHeroEffects(){
 heroEffectsObserver?.disconnect();heroEffectsObserver=null;heroOnscreen=true;
 const h=$('.hero');if(h&&'IntersectionObserver'in window){heroEffectsObserver=new IntersectionObserver(es=>{heroOnscreen=es[0].isIntersecting;syncHeroEffects();},{threshold:0});heroEffectsObserver.observe(h);}
 syncHeroEffects();
}
function setMotion(value){animationOn=value;document.documentElement.dataset.motion=value?'on':'off';$$('button[data-motion]').forEach(b=>{b.setAttribute('aria-pressed',String(value));b.textContent='Motion: '+(value?'on':'off');});if(model)model.setMotion(value);$$('[data-rain]').forEach(b=>b.setAttribute('aria-pressed',String(model?model.rain:value)));$$('[data-orbit]').forEach(b=>b.setAttribute('aria-pressed',String(model?model.orbit:value)));syncHeroEffects();}
function normalize(s){return s.toLowerCase().normalize('NFKD').replace(/[^a-z0-9\s]/g,' ');}
function filterJournal(){const q=normalize($('#journal-search')?.value||'').trim().split(/\s+/).filter(Boolean);let count=0;$$('.all-guides .article-card').forEach(c=>{const show=(journalCategory==='All'||c.dataset.category===journalCategory)&&q.every(t=>normalize(c.dataset.filtertext).includes(t));c.hidden=!show;if(show)count++;});$('.filter-count').textContent=count+' '+(count===1?'guide':'guides')+' to explore';$('.no-results').hidden=count>0;}
function searchSite(){const q=normalize($('#site-search').value).trim().split(/\s+/).filter(Boolean);const found=data.search.filter(x=>q.every(t=>normalize(x.title+' '+x.description+' '+x.category).includes(t)));$('.search-count').textContent=found.length+' results · Search runs in your browser.';$('.search-results').innerHTML=found.length?found.map(x=>`<a href="${pages?routeHash(x.route):relativeRoute(x.route)}" data-route="${x.route}"><small>${esc(x.category)}</small><b>${esc(x.title)} ${arrow}</b><p>${esc(x.description)}</p></a>`).join(''):'<p>No results yet. Try “drainage,” “rain,” “slab,” or “shower.”</p>';}
function routeHash(route,anchor=''){return '#'+new URLSearchParams({route,...(anchor?{section:anchor}:{})}).toString();}
function relativeRoute(route){const path=location.pathname;const root=(path.includes('/services/')?path.split('/services/')[0]:path.includes('/blog/')?path.split('/blog/')[0]:path.includes('/gallery/')?path.split('/gallery/')[0]:path.includes('/contact/')?path.split('/contact/')[0]:path.slice(0,path.lastIndexOf('/')));return root+route+(route.endsWith('/')?'index.html':'');}
function mediaURL(path){const key=path.split('/assets/')[1]||path.replace(/^assets\//,'');return media[key]||path;}
function inlineView(markup){return markup.replace(/src="([^"]+)"/g,(m,p)=>'src="'+mediaURL(p)+'"');}
function hydrateLinks(){
 if(pages)$$('a[data-route]').forEach(a=>a.href=routeHash(a.dataset.route,a.dataset.anchor||''));
 $$('.desktop-nav a[data-route],.mobile-links a[data-route]').forEach(a=>{if(a.dataset.route===activeRoute&&!a.dataset.anchor)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
}
function navigate(route,anchor='',push=true){
 if(!pages||!pages[route])return;
 if(expanded)toggleExpanded();closeDialogs();closeMenus();if(model){model.destroy();model=null;}if(sceneObserver){sceneObserver.disconnect();sceneObserver=null;}modelVisible=false;
 const p=pages[route];$('#main').outerHTML=inlineView(p.main);activeRoute=route;document.title=p.title;document.body.classList.toggle('home-page',route==='/');document.body.classList.toggle('inner-page',route!=='/');
 if(push)history.pushState({route,anchor},'',routeHash(route,anchor));initPage();
 requestAnimationFrame(()=>{const target=anchor&&document.getElementById(anchor);if(target)target.scrollIntoView({behavior:'instant',block:'start'});else{window.scrollTo({top:0,behavior:'instant'});$('#main').focus({preventScroll:true});}updateScroll();});
}
function initPage(){hydrateLinks();initHeroEffects();setMotion(animationOn);journalCategory='All';if($('.explorer-shell')){setZone(0);if('IntersectionObserver'in window){sceneObserver=new IntersectionObserver(entries=>{if(model)model.setVisible(entries[0].isIntersecting&&modelVisible);},{rootMargin:'100px'});sceneObserver.observe($('.model-stage'));}}if($('#journal-search'))filterJournal();updateScroll();}
function updateScroll(){
 document.documentElement.classList.toggle('scrolled',window.scrollY>70);
 const article=$('[data-page="article"]');const ratio=article?Math.min(1,Math.max(0,window.scrollY/Math.max(1,article.scrollHeight-innerHeight))):0;$('.reading-progress i').style.width=(ratio*100)+'%';
 if(article){let chosen=$('.article-section')?.id;for(const s of $$('.article-section'))if(s.getBoundingClientRect().top<190)chosen=s.id;$$('[data-toc]').forEach(a=>a.classList.toggle('active',a.dataset.toc===chosen));}
}
let scrollQueued=false;window.addEventListener('scroll',()=>{if(scrollQueued)return;scrollQueued=true;requestAnimationFrame(()=>{scrollQueued=false;updateScroll();});},{passive:true});
document.addEventListener('click',e=>{
 const t=e.target.closest?.('button,a,summary');if(!t)return;
 if(t.matches('[data-close]')){t.closest('dialog')?.close();return;}
 if(t.matches('[data-guide]')){guideStart(t.dataset.preset||'');return;}
 if(t.matches('[data-inquire]')){contactPanel();return;}
 if(t.matches('[data-answer]')){guide.answers[guide.step]=t.dataset.answer;$$('[data-answer]',dialogBody).forEach(b=>b.setAttribute('aria-pressed',String(b===t)));$('[data-next]').disabled=false;return;}
 if(t.matches('[data-next]')){if(guide.answers[guide.step]){guide.step++;renderGuide();}return;}
 if(t.matches('[data-back]')){if(guide.step){guide.step--;renderGuide();}else dialog.close();return;}
 if(t.matches('[data-result]')){renderResult();titleFocus();return;}
 if(t.matches('[data-download-brief]')){saveText(brief(),'Waterproofing360-project-brief.txt');notify('Project brief created. Nothing was submitted.');return;}
 if(t.matches('[data-copy-brief]')){copyText(brief(),$('.guide-notes'));return;}
 if(t.matches('[data-zone]')){setZone(Number(t.dataset.zone));return;}
 if(t.matches('[data-view]')){selectView(t.dataset.view);return;}
 if(t.matches('[data-mode]')){if(model){model.setMode(t.dataset.mode);$$('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b===t)));}return;}
 if(t.matches('[data-zoom]')){model?.zoom(Number(t.dataset.zoom));return;}
 if(t.matches('[data-rotate]')){model?.rotate(Number(t.dataset.rotate)*.26);$('[data-orbit]')?.setAttribute('aria-pressed','false');return;}
 if(t.matches('[data-reset]')){model?.reset();$$('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode==='cutaway')));return;}
 if(t.matches('[data-rain],[data-orbit]')){const on=t.getAttribute('aria-pressed')!=='true';if(!animationOn&&on){notify('Motion is turned off. Enable it in the footer to use animated rain or orbit.');return;}t.setAttribute('aria-pressed',String(on));if(t.hasAttribute('data-rain'))model?.setRain(on);else model?.setOrbit(on);return;}
 if(t.matches('[data-expand]')){toggleExpanded();return;}
 if(t.matches('[data-audience]')){setAudience(t.dataset.audience);return;}
 if(t.matches('[data-hero]')){$('.hero').dataset.scene=t.dataset.hero;$$('[data-hero]').forEach(b=>b.setAttribute('aria-pressed',String(b===t)));return;}
 if(t.matches('[data-motion]')){setMotion(!animationOn);return;}
 if(t.matches('[data-category-filter]')){journalCategory=t.dataset.categoryFilter;$$('[data-category-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===t)));filterJournal();return;}
 if(t.matches('[data-reset-filters]')){journalCategory='All';$('#journal-search').value='';$$('[data-category-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.categoryFilter==='All')));filterJournal();return;}
 if(t.matches('[data-checklist]'))return;
 if(t.matches('[data-menu]')){const m=$('#solutions-menu');m.hidden=!m.hidden;t.setAttribute('aria-expanded',String(!m.hidden));return;}
 if(t.matches('[data-mobile]')){openDialog(mobile);t.setAttribute('aria-expanded','true');return;}
 if(t.matches('[data-search]')){$('#site-search').value='';searchSite();openDialog(searchDialog);return;}
 if(t.matches('[data-share]')){copyText(location.href);return;}
 if(t.matches('[data-print]')){window.print();return;}
 if(t.matches('[data-release]')){dialogBody.innerHTML='<p class="kicker">Waterproofing360 / Release 5.0.0</p><h2 id="dialog-title">A working review.<br>A separate website.</h2><div class="release-copy"><p>This R5 preview uses the supplied company logo and starts Live 3D with rain and orbit on. Hero effects run by default without a hero pause button; reduced-motion preferences and the footer motion setting are respected. It contains the actual site implementation, eight sourced field guides, and a native 3D house model with WebGL, a depth-buffered compatibility renderer, and a detailed-image view.</p><p>The Gallery tab links to seven original service-specific project albums. Small job-site thumbnails come from the company’s original homepage service section. Architectural scenes and the 3D model remain illustrative, not records of completed projects or engineering details.</p><p>Search and guide interactions run locally. Guide choices are not sent automatically. Contact links open existing company channels only when selected.</p><p>The live waterproofing360.com website has not been changed by this build. Review indexing remains disabled until a production URL is explicitly configured.</p></div><div class="guide-nav"><button type="button" class="btn compact" data-close>Back to the site '+arrow+'</button></div>';openDialog(dialog);return;}
 if(t.matches('a[data-route]')){
  if(pages&&!e.metaKey&&!e.ctrlKey&&!e.shiftKey&&e.button===0){e.preventDefault();navigate(t.dataset.route,t.dataset.anchor||'');return;}closeMenus();closeDialogs();return;
 }
 if(t.matches('a[href^="#"]')&&t.hash.length>1&&!t.hash.startsWith('#route=')){
  const id=decodeURIComponent(t.hash.slice(1));const el=document.getElementById(id);if(el){e.preventDefault();el.scrollIntoView({behavior:animationOn?'smooth':'instant',block:'start'});if(pages)history.replaceState({route:activeRoute,anchor:id},'',routeHash(activeRoute,id));}return;
 }
 if(!t.closest('.menu-wrap'))closeMenus();
});
document.addEventListener('pointerdown',e=>{if(!e.target.closest('.menu-wrap'))closeMenus();});
document.addEventListener('input',e=>{if(e.target.id==='journal-search')filterJournal();if(e.target.id==='site-search')searchSite();});
document.addEventListener('change',e=>{if(e.target.matches('[data-checklist]')){$('.check-status').textContent=$$('[data-checklist]:checked').length+' of 4 items noted · This checklist stays in this page.';}});
document.addEventListener('keydown',e=>{
 if(e.key==='Escape'){if(expanded){e.preventDefault();toggleExpanded();}else closeMenus();}
 if((e.key==='/'||((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'))&&!e.target.matches('input,textarea,select')&&!$('dialog[open]')){e.preventDefault();$('#site-search').value='';searchSite();openDialog(searchDialog);}
 if(e.target.matches('.zone-tab')&&['ArrowRight','ArrowLeft','ArrowDown','ArrowUp','Home','End'].includes(e.key)){e.preventDefault();const n=e.key==='Home'?0:e.key==='End'?4:(zone+(['ArrowRight','ArrowDown'].includes(e.key)?1:4))%5;setZone(n,true);return;}
 if(e.target.matches('[data-audience]')&&['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const ks=Object.keys(audiences);const i=ks.indexOf(e.target.dataset.audience);setAudience(ks[e.key==='Home'?0:e.key==='End'?2:(i+(e.key==='ArrowRight'?1:2))%3],true);return;}
 if(expanded&&e.key==='Tab'){
  const f=$$('button:not([disabled]),a[href],canvas[tabindex]', $('.explorer-shell')).filter(x=>x.getClientRects().length);const first=f[0],last=f[f.length-1];if(e.shiftKey&&e.target===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&e.target===last){e.preventDefault();first.focus();}
 }
});
matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change',e=>{if(e.matches)setMotion(false);});
window.addEventListener('resize',()=>{if(innerWidth>1100&&mobile.open)mobile.close();},{passive:true});
document.addEventListener('visibilitychange',()=>{syncHeroEffects();if(model)model.setVisible(!document.hidden&&modelVisible);});
if(pages){const restore=()=>{const p=new URLSearchParams(location.hash.slice(1));const r=p.get('route')||'/';navigate(pages[r]?r:'/',p.get('section')||'',false);};window.addEventListener('popstate',restore);if(location.hash.startsWith('#route='))restore();else initPage();}else initPage();
setMotion(animationOn);
window.W360_DEBUG={getModel:()=>model,getRoute:()=>activeRoute,getZone:()=>zone,getMotion:()=>animationOn};
})();
