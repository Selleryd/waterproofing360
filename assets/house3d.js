/* Native WebGL concept house. Original procedural geometry; no external engine or runtime.
   Real orbit, perspective projection, exploded layers, and view-anchored controls.
   This visual model is not an engineering specification or an installation detail. */
(() => {
'use strict';
const TAU=Math.PI*2,clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
const sub=(a,b)=>a.map((v,i)=>v-b[i]),dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const norm=a=>{const n=Math.hypot(...a)||1;return a.map(v=>v/n);};
function mul(a,b){const o=new Float32Array(16);for(let c=0;c<4;c++)for(let r=0;r<4;r++)for(let k=0;k<4;k++)o[c*4+r]+=a[k*4+r]*b[c*4+k];return o;}
function perspective(fov,aspect,near,far){const f=1/Math.tan(fov/2);return new Float32Array([f/aspect,0,0,0,0,f,0,0,0,0,(far+near)/(near-far),-1,0,0,2*far*near/(near-far),0]);}
function look(eye,at){const z=norm(sub(eye,at)),x=norm(cross([0,1,0],z)),y=cross(z,x);return new Float32Array([x[0],y[0],z[0],0,x[1],y[1],z[1],0,x[2],y[2],z[2],0,-dot(x,eye),-dot(y,eye),-dot(z,eye),1]);}
const color=h=>[(h>>16&255)/255,(h>>8&255)/255,(h&255)/255];
class Geometry{
 constructor(){this.v=[];}
 vertex(p,n,c,type,zone,level,shell){this.v.push(...p,...n,...c,type,zone,level,shell);}
 tri(a,b,c,col,type=0,zone=-1,level=0,shell=0,normals=null){const n=norm(cross(sub(b,a),sub(c,a))),rgb=color(col);[a,b,c].forEach((p,i)=>this.vertex(p,normals?normals[i]:n,rgb,type,zone,level,shell));}
 quad(a,b,c,d,col,type=0,zone=-1,level=0,shell=0){this.tri(a,b,c,col,type,zone,level,shell);this.tri(a,c,d,col,type,zone,level,shell);}
 box(x,y,z,w,h,d,col,type=0,zone=-1,level=0,shell=0){let X=w/2,Y=h/2,Z=d/2;const p=(a,b,c)=>[x+a*X,y+b*Y,z+c*Z];const q=(a,b,c,d)=>this.quad(p(...a),p(...b),p(...c),p(...d),col,type,zone,level,shell);
 q([-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]);q([1,-1,-1],[-1,-1,-1],[-1,1,-1],[1,1,-1]);q([1,-1,1],[1,-1,-1],[1,1,-1],[1,1,1]);q([-1,-1,-1],[-1,-1,1],[-1,1,1],[-1,1,-1]);q([-1,1,1],[1,1,1],[1,1,-1],[-1,1,-1]);q([-1,-1,-1],[1,-1,-1],[1,-1,1],[-1,-1,1]);}
 sphere(x,y,z,rx,ry,rz,col,type=0,zone=-1,level=0,shell=0,steps=12){
 const pt=(u,v)=>[x+rx*Math.sin(v)*Math.cos(u),y+ry*Math.cos(v),z+rz*Math.sin(v)*Math.sin(u)];const nn=p=>norm([(p[0]-x)/(rx*rx),(p[1]-y)/(ry*ry),(p[2]-z)/(rz*rz)]);
 for(let i=0;i<steps;i++)for(let j=0;j<steps*2;j++){const a=pt(j/steps/2*TAU,i/steps*Math.PI),b=pt((j+1)/steps/2*TAU,i/steps*Math.PI),c=pt((j+1)/steps/2*TAU,(i+1)/steps*Math.PI),d=pt(j/steps/2*TAU,(i+1)/steps*Math.PI);this.tri(a,b,c,col,type,zone,level,shell,[nn(a),nn(b),nn(c)]);this.tri(a,c,d,col,type,zone,level,shell,[nn(a),nn(c),nn(d)]);}}
 pipe(a,b,r,col,type=7,zone=-1,level=0,shell=0,n=12){const axis=norm(sub(b,a));const side=norm(cross(axis,Math.abs(axis[1])>.9?[1,0,0]:[0,1,0]));const other=norm(cross(axis,side));const point=(p,t)=>p.map((v,i)=>v+r*(side[i]*Math.cos(t)+other[i]*Math.sin(t)));for(let j=0;j<n;j++){const t=j/n*TAU,u=(j+1)/n*TAU;this.quad(point(a,t),point(b,t),point(b,u),point(a,u),col,type,zone,level,shell);this.tri(a,point(a,u),point(a,t),col,type,zone,level,shell);this.tri(b,point(b,t),point(b,u),col,type,zone,level,shell);}}
}
function buildHouse(){
 const m=new Geometry();const b=(...a)=>m.box(...a);const tube=(...a)=>m.pipe(...a);
 const concrete=0xc6c9c5,stone=0xb6b7ae,ivory=0xe7e4da,wood=0xa9865c,slate=0x27343d,blue=0x137fc1,metal=0x344957;
 // A cut soil plinth, layered aggregate, and an exposed foundation. Scale is conceptual.
 b(0,-2.2,0,13.5,.65,9.4,0x9b9384,2);b(0,-1.96,0,13.3,.16,9.2,0xb1aaa0,2);
 b(-5.5,-.61,-.2,2.4,2.62,8.3,0x999184,2);b(-5.5,.72,-.2,2.4,.11,8.3,0x6e8570,3);
 b(.3,-.61,-3.75,9.3,2.62,1.2,0x979283,2);b(.3,.73,-3.75,9.3,.1,1.2,0x728a73,3);
 b(5.45,-.61,-.45,2.9,2.62,8.3,0x9e988a,2);b(5.45,.74,-.45,2.9,.11,8.3,0xb9b9b0,2);
 // Membrane and floor layers separated in exploded mode.
 b(0,-1.62,0,8.25,.22,5.8,0xb9b7a8,2,-1,.1);
 b(0,-1.475,0,8.17,.055,5.7,0x1e78a5,6,3,.45);
 b(0,-1.31,0,8.05,.27,5.62,concrete,2,3,.9);
 b(0,-1.151,0,7.65,.047,5.27,0xdddcd3,2,3,.9);
 // Back and left basement walls remain visible in the cutaway.
 b(0,-.25,-2.7,8.3,2.1,.29,concrete,2,0,0);b(-4,-.25,0,.3,2.1,5.42,concrete,2,0,0);
 b(-4.185,-.3,0,.06,2.15,5.53,blue,6,0,0);b(0,-.3,-2.89,8.3,2.15,.06,blue,6,0,0);
 b(-4,-1.49,0,.8,.32,5.9,0xb4b7b2,2,0);b(0,-1.49,-2.7,8.85,.32,.75,0xb4b7b2,2,0);
 // Short return illustrates exposed membrane without hiding the room.
 b(-3.55,-.38,2.57,.85,1.94,.18,0xb3b9b6,2,0);b(-3.55,-.38,2.68,.85,1.96,.055,blue,6,0);
 // Exterior enclosure, omitted in cutaway/exploded mode.
 b(0,-.25,2.7,8.3,2.1,.29,concrete,2,0,0,1);b(4,-.25,0,.3,2.1,5.42,concrete,2,0,0,1);
 // Perimeter collection illustration and a sealed sump with a discharge riser.
 tube([-3.63,-1.02,-2.36],[-3.63,-1.02,2.15],.068,blue,7,1,.9);
 tube([-3.63,-1.02,2.15],[3.0,-1.02,2.15],.068,blue,7,1,.9);
 tube([3,-1.02,2.15],[3,-1.02,-1.25],.068,blue,7,1,.9);
 m.pipe([3,-1.12,-1.65],[3,-.67,-1.65],.37,0x334550,7,1,.9,0,24);
 m.pipe([3,-.67,-1.65],[3,-.59,-1.65],.4,0x486472,7,1,.9,0,24);
 tube([3,-.57,-1.65],[3,.55,-1.65],.063,0x657780,7,1,.9);tube([3,.55,-1.65],[4.35,.55,-1.65],.063,0x657780,7,1,.9);
 // Concrete crack as a narrow line on the internal rear wall; not a structural diagnosis.
 const crack=[[-1.9,.68,-2.541],[-1.7,.25,-2.541],[-1.9,-.04,-2.541],[-1.6,-.37,-2.541],[-1.7,-.69,-2.541],[-1.5,-1.15,-2.541]];
 for(let i=0;i<crack.length-1;i++)tube(crack[i],crack[i+1],.018,0x44505a,0,2,0,0,6);
 for(let i=1;i<4;i++)m.pipe([crack[i][0],crack[i][1],-2.53],[crack[i][0],crack[i][1],-2.44],.028,0x1b8bcc,7,2,0,0,8);
 // Basement shelves and a support post.
 b(-2.55,-.62,-1.83,1.35,.08,.5,0x927653,1);b(-2.55,-.07,-1.83,1.35,.06,.5,0x927653,1);
 for(const x of [-3.15,-1.95])tube([x,-1.1,-1.8],[x,.29,-1.8],.026,metal);
 b(-2.8,-.35,-1.85,.4,.42,.34,0xbda785,1);b(-2.25,-.4,-1.85,.44,.31,.35,0xa6adab,2);
 b(.3,-.22,.35,.25,2.17,.25,0xb2b8b4,2);
 // The principal occupied floor, timber ceiling edge and recessed glazing frames.
 b(0,.89,0,8.65,.26,5.95,0xc6cbc8,2,-1,1.4);b(0,1.05,0,8.2,.055,5.5,0xc6aa83,1,-1,1.4);
 b(0,2.28,-2.62,8.1,2.45,.22,ivory,2,-1,1.4);b(-3.96,2.28,0,.24,2.45,5.4,0xa98764,1,-1,1.4);
 // Narrow architectural columns and floor-to-ceiling exterior glass; shell disappears on cutaway.
 for(const x of [-3.85,-.75,3.85])b(x,2.3,2.67,.12,2.5,.11,metal,7,-1,1.4);
 for(const z of [-2.5,.25,2.65])b(3.95,2.3,z,.12,2.5,.12,metal,7,-1,1.4);
 b(.0,2.28,2.7,7.8,2.38,.035,0x71959e,4,-1,1.4,1);b(3.99,2.28,0,.035,2.38,5.4,0x6b8f9c,4,-1,1.4,1);
 // Living room rug, soft cushions, low table, fireplace, kitchen and cabinet handles.
 b(-.75,1.09,.75,3.3,.03,2.3,0xe5e0d1,0,-1,1.4);
 b(-1.0,1.34,.8,2.35,.35,.84,0xe5ded0,0,-1,1.4);
 b(-1.0,1.68,.48,2.45,.65,.25,0xcec8bc,0,-1,1.4);
 for(const x of [-2.1,.1])b(x,1.57,.84,.25,.61,.91,0xded6c5,0,-1,1.4);
 for(const x of [-1.7,-.9,-.18])m.sphere(x,1.56,.96,.35,.16,.34,0xeee6d5,0,-1,1.4,0,6);
 b(-1.57,1.87,.59,.43,.37,.14,0x314e64,0,-1,1.4);b(-.45,1.87,.59,.43,.37,.14,0x8ba8b4,0,-1,1.4);
 b(-.65,1.42,1.98,1.18,.13,.48,0x8d7658,1,-1,1.4);for(const x of [-1.1,-.2])b(x,1.25,1.98,.06,.3,.34,metal,7,-1,1.4);
 b(1.1,1.89,-2.37,1.9,1.6,.26,0x62747e,2,-1,1.4);b(1.1,1.53,-2.205,1.4,.47,.045,0x102431,0,-1,1.4);
 b(1.1,1.35,-2.16,.95,.05,.09,0xf6bc64,9,-1,1.4);
 b(-2.1,1.7,-2.03,2.8,1.17,.9,0x9d815e,1,-1,1.4);b(-2.1,2.33,-2.03,2.91,.09,.96,0xd5d9d4,2,-1,1.4);
 for(const x of [-3,-2.15,-1.35])b(x,1.97,-1.56,.35,.025,.04,metal,7,-1,1.4);
 b(-2.22,2.389,-2.03,.68,.02,.46,0x3b535d,7,-1,1.4);tube([-2.37,2.36,-2.24],[-2.37,2.74,-2.24],.023,0xbcc8c7,7,-1,1.4);tube([-2.37,2.74,-2.24],[-2.13,2.74,-2.24],.023,0xbcc8c7,7,-1,1.4);
 // Interior wall art.
 b(-1.13,2.92,-2.482,1.03,.75,.055,0x415664,0,-1,1.4);b(-1.13,2.92,-2.442,.93,.65,.02,0xd6d8ca,0,-1,1.4);b(-1.25,2.94,-2.426,.4,.22,.012,0x7b92a1,0,-1,1.4);
 // Second floor cutaway: bedroom left, glass shower right, generous balcony on the front.
 b(0,3.61,0,8.7,.23,6.02,0xc6cbc8,2,-1,2.8);b(0,3.76,0,8.15,.04,5.5,0xcbb798,1,-1,2.8);
 b(0,4.94,-2.6,8.2,2.37,.23,ivory,2,-1,2.8);b(-3.98,4.94,0,.23,2.37,5.38,0xa28360,1,-1,2.8);
 b(.3,4.94,-.7,.18,2.37,3.77,0xe2dfd4,2,-1,2.8);
 // Bed, layered linens, pillows and lamps.
 b(-1.98,3.98,-.55,2.35,.37,2.36,0xa68963,1,-1,2.8);b(-1.98,4.24,-.5,2.18,.29,2.2,0xe1dfd6,0,-1,2.8);b(-1.98,4.45,-1.63,2.32,1.11,.17,0xb2a38d,1,-1,2.8);
 b(-1.98,4.425,.0,2.19,.1,1.11,0x647d8e,0,-1,2.8);
 for(const x of [-2.48,-1.49])m.sphere(x,4.51,-1.15,.43,.17,.33,0xf1eee3,0,-1,2.8,0,7);
 for(const x of [-3.46,-.53]){b(x,4.1,-1.33,.44,.7,.53,0x977c59,1,-1,2.8);tube([x,4.47,-1.33],[x,4.71,-1.33],.025,0x61717b,7,-1,2.8);m.sphere(x,4.84,-1.33,.2,.18,.2,0xf5d7a1,9,-1,2.8,0,6);}
 // Shower base, drain, waterproof panel and plumbing fixtures.
 b(2.0,3.805,-1.3,2.35,.07,2.3,0x3188ad,6,4,2.8);b(2.0,3.86,-1.3,2.2,.05,2.15,0xccd4ce,2,4,2.8);
 b(2,4.9,-2.449,2.55,2.08,.065,0xc4d2d2,2,4,2.8);
 b(2.0,3.9,-1.89,.62,.021,.085,metal,7,4,2.8);
 b(3.24,4.83,-1.3,.04,1.93,2.05,0x9bc0ca,4,4,2.8);b(2.19,4.83,-.27,1.9,1.93,.04,0x97b6c0,4,4,2.8);
 tube([1.94,4.0,-2.36],[1.94,5.54,-2.36],.022,0xdce2da,7,4,2.8);tube([1.94,5.54,-2.36],[1.94,5.54,-1.85],.027,0xdce2da,7,4,2.8);b(1.94,5.52,-1.72,.43,.04,.37,metal,7,4,2.8);
 b(1.94,4.42,-2.34,.22,.17,.06,metal,7,4,2.8);
 // Balcony safety railing: slim posts, transparent-looking blue glazing.
 for(const x of [-3.98,-1.3,1.4,3.98])b(x,4.23,2.78,.035,.84,.035,metal,7,-1,2.8);
 b(0,4.68,2.78,8.02,.04,.04,metal,7,-1,2.8);b(0,4.27,2.8,7.95,.74,.02,0x9bb6be,4,-1,2.8);
 b(0,4.95,2.22,7.8,2.31,.025,0x7f9ca7,4,-1,2.8,1);b(4.04,4.95,-.2,.025,2.31,4.94,0x7e9aa5,4,-1,2.8,1);
 // Roof, soffit, slim fascia and warm recessed lines.
 b(0,6.25,-.12,9.25,.28,6.55,slate,5,-1,4,2);b(0,6.084,-.12,8.98,.07,6.3,wood,1,-1,4,2);
 b(0,6.066,2.64,7.8,.025,.043,0xffdfa0,9,-1,4,2);b(4.17,6.066,0,.035,.025,4.8,0xffdfa0,9,-1,4,2);
 // Paving on the right and a framed pool. No depicted installation performance is implied.
 for(let i=0;i<3;i++)for(let j=0;j<7;j++)b(4.75+i*.72,.82,-2.72+j*.78,.69,.045,.75,0xc1c4bd,2);
 b(5.28,.855,.7,2.63,.11,4.8,0xd5d8ce,2,4);b(5.28,.91,.7,2.28,.034,4.38,0x3c9db9,4,4);
 for(let i=0;i<4;i++){b(3.68+i*.035,.61-i*.28,3.3+i*.4,1.68,.16,.65,0xb5b9b0,2);}
 // A few small shrubs and trees give the model architectural scale without blocking cutaway details.
 const plant=(x,z,size=1)=>{m.pipe([x,.82,z],[x,1.3,z],.11*size,0x496474,7);m.sphere(x,1.53,z,.44*size,.55*size,.4*size,0x557667,3,-1,0,0,8);};
 plant(-5.35,2.82,.78);plant(-5.53,-2.77,.98);plant(6.44,-3.42,.67);
 m.pipe([-5.66,.8,-1.3],[-5.66,3.5,-1.3],.07,0x776b55,1);m.sphere(-5.66,3.95,-1.3,.61,1.4,.63,0x547766,3,-1,0,0,9);
 // Indoor planting adds softer scale cues.
 m.pipe([2.7,1.08,1.13],[2.7,1.42,1.13],.19,0x647d82,2,-1,1.4);m.sphere(2.7,1.86,1.13,.32,.61,.3,0x55765c,3,-1,1.4,0,7);
 return m;
}
const VS=`precision highp float;
attribute vec3 aPosition;attribute vec3 aNormal;attribute vec3 aColor;attribute float aType;attribute float aZone;attribute float aLevel;attribute float aShell;
uniform mat4 uMVP;uniform float uExplode;uniform mediump float uTime;
varying mediump vec3 vP;varying mediump vec3 vN;varying mediump vec3 vC;varying mediump float vType;varying mediump float vZone;varying mediump float vShell;
void main(){vec3 p=aPosition;p.y+=aLevel*uExplode;if(aType>9.5){p.y=9.8-mod(aPosition.y+uTime*4.2,12.3);p.x+=.15*sin(uTime);}vP=p;vN=aNormal;vC=aColor;vType=aType;vZone=aZone;vShell=aShell;gl_Position=uMVP*vec4(p,1.);}`;
const FS=`precision mediump float;
varying mediump vec3 vP;varying mediump vec3 vN;varying mediump vec3 vC;varying mediump float vType;varying mediump float vZone;varying mediump float vShell;
uniform vec3 uEye;uniform float uMode;uniform float uZone;uniform mediump float uTime;
float noise(vec3 p){return fract(sin(dot(p,vec3(127.1,311.7,74.7)))*43758.5453);}
void main(){
 if(uMode>.5&&vShell>.5&&vShell<1.5)discard;
 if(uMode>.5&&uMode<1.5&&vShell>1.5)discard;
 if(vType>9.5){gl_FragColor=vec4(.31,.57,.71,.5);return;}
 vec3 n=normalize(vN);if(!gl_FrontFacing)n=-n;vec3 c=vC;float t=vType;
 float grain=noise(floor(vP*220.));
 if(t>.5&&t<1.5){float wood=.8+.11*sin(vP.x*26.+sin(vP.z*2.)*.7)+.05*grain;c*=wood;}
 if(t>1.5&&t<2.5){c*=.94+.1*grain;float mortar=step(.989,fract(vP.y*2.3));c*=1.-.07*mortar;}
 if(t>2.5&&t<3.5){c*=.8+.25*grain;}
 if(t>3.5&&t<4.5){float ripple=sin(vP.x*8.+uTime)*sin(vP.z*10.-uTime*.7);c+=vec3(.06,.12,.14)*ripple;c=mix(c,vec3(.82,.9,.91),pow(max(0.,n.y),2.)*.17);}
 if(t>4.5&&t<5.5){c*=.82+.13*grain;float lines=step(.92,fract(vP.x*8.));c*=1.-.13*lines;}
 if(t>5.5&&t<6.5){float studs=step(.78,fract(vP.y*15.))*step(.78,fract((abs(n.x)>.5?vP.z:vP.x)*15.));c*=.84+.22*studs;}
 vec3 light=normalize(vec3(-.3,1.,.6));float shade=.52+.47*max(0.,dot(n,light));shade*=.94+.06*max(0.,n.y);
 c*=shade;vec3 v=normalize(uEye-vP);float spec=pow(max(0.,dot(reflect(-light,n),v)),28.);
 if(t>3.5&&t<4.5)c+=vec3(.3,.37,.38)*spec;if(t>6.5&&t<7.5)c+=vec3(.27)*spec;
 float warm=exp(-length(vP-vec3(-1.,2.7,-1.))*.8)*.12+exp(-length(vP-vec3(-2.,5.,-1.)))*.09;c+=vec3(.95,.55,.17)*warm;
 if(vZone>-.5&&abs(vZone-uZone)<.4){c=mix(c,vec3(.12,.51,.88),.23);c+=vec3(.025,.05,.085);}
 if(t>8.5&&t<9.5)c=vC;
 c=pow(max(c,vec3(0.)),vec3(.9));gl_FragColor=vec4(c,1.);
}`;
class House{
 constructor(canvas,pins,select){
  this.canvas=canvas;this.pinRoot=pins;this.select=select;this.visible=true;this.motion=true;this.orbit=true;this.rain=true;this.yaw=.61;this.elev=.37;this.distance=21.0;this.mode='cutaway';this.zone=0;this.explode=0;this.targetExplode=0;this.raf=0;this.time=0;this.prev=0;this.dead=false;this.drag=null;this.abort=new AbortController();
  const mesh=buildHouse();this.count=mesh.v.length/13;
  const gl=canvas.getContext('webgl',{antialias:true,alpha:false,powerPreference:'low-power'});this.gl=gl;
  if(gl){
   this.renderer='webgl';
   const shader=(type,source)=>{const sh=gl.createShader(type);gl.shaderSource(sh,source);gl.compileShader(sh);if(!gl.getShaderParameter(sh,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(sh));return sh;};
   const program=gl.createProgram(),vs=shader(gl.VERTEX_SHADER,VS),fs=shader(gl.FRAGMENT_SHADER,FS);gl.attachShader(program,vs);gl.attachShader(program,fs);gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(program));gl.deleteShader(vs);gl.deleteShader(fs);this.program=program;gl.useProgram(program);
   this.u={};for(const n of ['uMVP','uExplode','uTime','uEye','uMode','uZone'])this.u[n]=gl.getUniformLocation(program,n);
   this.buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,this.buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(mesh.v),gl.STATIC_DRAW);
   this.attrs=[['aPosition',3,0],['aNormal',3,3],['aColor',3,6],['aType',1,9],['aZone',1,10],['aLevel',1,11],['aShell',1,12]].map(([n,size,offset])=>[gl.getAttribLocation(program,n),size,offset]);
   this.rainBuffer=gl.createBuffer();let drops=[];for(let i=0;i<130;i++){const x=Math.sin(i*29.12)*8,z=Math.sin(i*18.6)*5,y=(i*.71)%12;for(const dy of [0,.29])drops.push(x,y+dy,z,0,1,0,.5,.7,.8,10,-1,0,0);}gl.bindBuffer(gl.ARRAY_BUFFER,this.rainBuffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(drops),gl.STATIC_DRAW);this.rainCount=drops.length/13;
  }else{
   // Real perspective-projected mesh fallback, not a substituted screenshot.
   // This retains orbit, zoom and exploded layers when WebGL is unavailable.
   this.renderer='canvas3d';this.ctx=canvas.getContext('2d',{alpha:false});
   if(!this.ctx)throw Error('Canvas graphics unavailable');
   this.faces=[];
   for(let i=0;i<mesh.v.length;i+=39){const v=mesh.v;const ps=[[v[i],v[i+1],v[i+2]],[v[i+13],v[i+14],v[i+15]],[v[i+26],v[i+27],v[i+28]]];
    this.faces.push({p:ps,n:norm([v[i+3]+v[i+16]+v[i+29],v[i+4]+v[i+17]+v[i+30],v[i+5]+v[i+18]+v[i+31]]),c:v.slice(i+6,i+9),type:v[i+9],zone:v[i+10],level:v[i+11],shell:v[i+12]});
   }
  }
  this.anchors=[[-3.85,-.13,2.63,0],[3.,-.8,1.63,.9],[-1.75,-.1,-2.42,0],[.12,-1.4,2.,.9],[2.2,4.85,-.21,2.8]];
  pins.innerHTML=this.anchors.map((_,i)=>`<button type="button" class="hotspot" data-zone="${i}" aria-label="Explore ${['exterior foundations','drainage and collection','cracks and openings','beneath the slab','specialty wet areas'][i]}" aria-pressed="${i===0}">0${i+1}</button>`).join('');this.pinButtons=Array.from(pins.children);
  const options={signal:this.abort.signal};
  canvas.addEventListener('pointerdown',e=>{if(e.button!==0)return;this.drag={id:e.pointerId,x:e.clientX,y:e.clientY,type:e.pointerType};canvas.setPointerCapture(e.pointerId);this.orbit=false;document.querySelector('[data-orbit]')?.setAttribute('aria-pressed','false');},options);
  canvas.addEventListener('pointermove',e=>{if(!this.drag||e.pointerId!==this.drag.id)return;const dx=e.clientX-this.drag.x,dy=e.clientY-this.drag.y;this.yaw-=dx*.006;if(this.drag.type!=='touch')this.elev=clamp(this.elev+dy*.004,.12,1.0);this.drag.x=e.clientX;this.drag.y=e.clientY;this.request();},options);
  for(const n of ['pointerup','pointercancel','lostpointercapture'])canvas.addEventListener(n,()=>this.drag=null,options);
  canvas.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','-','=','Home'].includes(e.key)){e.preventDefault();if(e.key==='Home')this.reset();else if(['+','='].includes(e.key))this.zoom(1);else if(e.key==='-')this.zoom(-1);else if(e.key==='ArrowLeft')this.rotate(-.15);else if(e.key==='ArrowRight')this.rotate(.15);else{this.elev=clamp(this.elev+(e.key==='ArrowUp'?.08:-.08),.12,1.0);this.request();}}},options);
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();this.visible=false;cancelAnimationFrame(this.raf);document.querySelector('.model-status').textContent='3D graphics paused. Switch to the detailed cutaway or reload to restore the model.';},options);
  this.resizeObserver=new ResizeObserver(()=>this.resize());this.resizeObserver.observe(canvas);this.resize();
 }
 renderSoftware(matrix,eye){
  // A depth-buffered CPU fallback renders the same 3D geometry. It avoids
  // painter-order artifacts and preserves all camera/layer interactions.
  const ctx=this.ctx,ratio=Math.min(1,900/this.canvas.width),w=Math.max(1,Math.round(this.canvas.width*ratio)),h=Math.max(1,Math.round(this.canvas.height*ratio));
  if(!this.softCanvas){this.softCanvas=document.createElement('canvas');this.softCtx=this.softCanvas.getContext('2d');}
  if(this.softCanvas.width!==w||this.softCanvas.height!==h){this.softCanvas.width=w;this.softCanvas.height=h;this.softImage=this.softCtx.createImageData(w,h);this.depth=new Float32Array(w*h);}
  const pix=this.softImage.data,depth=this.depth;depth.fill(Infinity);
  for(let i=0;i<pix.length;i+=4){pix[i]=232;pix[i+1]=239;pix[i+2]=241;pix[i+3]=255;}
  const project=p=>{const x=p[0],y=p[1],z=p[2],d=matrix[3]*x+matrix[7]*y+matrix[11]*z+matrix[15];return [(matrix[0]*x+matrix[4]*y+matrix[8]*z+matrix[12])/d*w/2+w/2,h/2-(matrix[1]*x+matrix[5]*y+matrix[9]*z+matrix[13])/d*h/2,(matrix[2]*x+matrix[6]*y+matrix[10]*z+matrix[14])/d,d];};
  const light=norm([-.3,1,.6]);
  for(const f of this.faces){
   if(this.mode!=='exterior'&&f.shell===1)continue;if(this.mode==='cutaway'&&f.shell===2)continue;
   const pts=f.p.map(p=>[p[0],p[1]+f.level*this.explode,p[2]]),v=pts.map(project);if(v.some(p=>p[3]<=.1))continue;
   const x0=v[0][0],y0=v[0][1],x1=v[1][0],y1=v[1][1],x2=v[2][0],y2=v[2][1],den=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2);if(Math.abs(den)<.01)continue;
   const minX=Math.max(0,Math.floor(Math.min(x0,x1,x2))),maxX=Math.min(w-1,Math.ceil(Math.max(x0,x1,x2))),minY=Math.max(0,Math.floor(Math.min(y0,y1,y2))),maxY=Math.min(h-1,Math.ceil(Math.max(y0,y1,y2)));if(minX>maxX||minY>maxY)continue;
   let n=f.n;const mid=[(pts[0][0]+pts[1][0]+pts[2][0])/3,(pts[0][1]+pts[1][1]+pts[2][1])/3,(pts[0][2]+pts[1][2]+pts[2][2])/3];if(dot(n,sub(eye,mid))<0)n=n.map(x=>-x);
   let shade=(.58+.42*Math.max(0,dot(n,light)))*(.94+.06*Math.max(0,n[1])),c=f.c.map(v=>v*shade);
   if(f.type===1)c=c.map(v=>v*(.93+.025*Math.sin(mid[0]*17+mid[2]*3)));
   if(f.type===4)c=c.map((v,i)=>v+[.05,.08,.09][i]*Math.max(0,n[1]));
   if(f.type===6)c=c.map(v=>v*.94);if(f.zone===this.zone)c=c.map((v,i)=>v*.77+[.12,.51,.88][i]*.23+[.025,.05,.085][i]);if(f.type===9)c=f.c;
   c=c.map(v=>Math.round(255*Math.pow(clamp(v,0,1),.9)));
   const dxA=(y1-y2)/den,dyA=(x2-x1)/den,dxB=(y2-y0)/den,dyB=(x0-x2)/den,z0=v[0][2],z1=v[1][2],z2=v[2][2];
   for(let y=minY;y<=maxY;y++){let a=((y1-y2)*(minX+.5-x2)+(x2-x1)*(y+.5-y2))/den,b=((y2-y0)*(minX+.5-x2)+(x0-x2)*(y+.5-y2))/den;
    for(let x=minX;x<=maxX;x++,a+=dxA,b+=dxB){const d=1-a-b;if(a<-.0001||b<-.0001||d<-.0001)continue;const z=a*z0+b*z1+d*z2,j=y*w+x;if(z>=depth[j])continue;depth[j]=z;const k=j*4;pix[k]=c[0];pix[k+1]=c[1];pix[k+2]=c[2];}
   }
  }
  this.softCtx.putImageData(this.softImage,0,0);ctx.imageSmoothingEnabled=true;ctx.drawImage(this.softCanvas,0,0,this.canvas.width,this.canvas.height);
  if(this.rain&&this.motion){ctx.save();ctx.scale(this.canvas.width/w,this.canvas.height/h);ctx.strokeStyle='rgba(54,123,158,.42)';ctx.lineWidth=.8;ctx.beginPath();for(let i=0;i<95;i++){const y=9.8-((i*.71+this.time*4.2)%12.3),a=project([Math.sin(i*29.12)*8,y,Math.sin(i*18.6)*5]),b=project([Math.sin(i*29.12)*8,y+.29,Math.sin(i*18.6)*5]);ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);}ctx.stroke();ctx.restore();}
 }
 bind(buffer){const gl=this.gl;gl.bindBuffer(gl.ARRAY_BUFFER,buffer);for(const [loc,size,offset] of this.attrs){if(loc<0)continue;gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,size,gl.FLOAT,false,52,offset*4);}}
 resize(){if(this.dead)return;const c=this.canvas,d=Math.min(devicePixelRatio||1,1.6),w=Math.max(1,c.clientWidth),h=Math.max(1,c.clientHeight);c.width=Math.round(w*d);c.height=Math.round(h*d);this.aspect=w/h;this.request();}
 request(){if(!this.visible||this.dead||this.raf)return;this.raf=requestAnimationFrame(t=>this.render(t));}
 render(now){this.raf=0;if(!this.visible||this.dead)return;const gl=this.gl,dt=Math.min(.05,this.prev?(now-this.prev)/1000:.016);this.prev=now;
  if(this.motion){this.time+=dt;if(this.orbit)this.yaw+=dt*.15;this.explode+=(this.targetExplode-this.explode)*Math.min(1,dt*7);}else this.explode=this.targetExplode;
  const wide=this.aspect>1.2;const distance=this.distance+(wide?0:1.6)+this.explode*8;const target=[.48,1.6+this.explode*1.7,.05];const eye=[target[0]+Math.sin(this.yaw)*Math.cos(this.elev)*distance,target[1]+Math.sin(this.elev)*distance,target[2]+Math.cos(this.yaw)*Math.cos(this.elev)*distance];
  const mvp=mul(perspective(.68,this.aspect,.1,80),look(eye,target));this.mvp=mvp;this.eye=eye;
  if(this.renderer==='canvas3d')this.renderSoftware(mvp,eye);else{
  gl.viewport(0,0,this.canvas.width,this.canvas.height);gl.clearColor(.905,.935,.944,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.disable(gl.CULL_FACE);gl.depthMask(true);gl.disable(gl.BLEND);gl.useProgram(this.program);gl.uniformMatrix4fv(this.u.uMVP,false,mvp);gl.uniform1f(this.u.uExplode,this.explode);gl.uniform1f(this.u.uTime,this.rain&&this.motion?this.time:0);gl.uniform3fv(this.u.uEye,eye);gl.uniform1f(this.u.uZone,this.zone);gl.uniform1f(this.u.uMode,this.mode==='exterior'?0:this.mode==='cutaway'?1:2);this.bind(this.buffer);gl.drawArrays(gl.TRIANGLES,0,this.count);
  if(this.rain&&this.motion){gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.depthMask(false);this.bind(this.rainBuffer);gl.drawArrays(gl.LINES,0,this.rainCount);gl.depthMask(true);gl.disable(gl.BLEND);}
  }
  this.anchors.forEach((a,i)=>{const p=[a[0],a[1]+a[3]*this.explode,a[2],1];const v=[0,0,0,0];for(let r=0;r<4;r++)for(let k=0;k<4;k++)v[r]+=mvp[k*4+r]*p[k];const x=(v[0]/v[3]*.5+.5)*100,y=(.5-v[1]/v[3]*.5)*100;const b=this.pinButtons[i];b.style.left=x+'%';b.style.top=y+'%';b.hidden=v[3]<0||x<2||x>98||y<4||y>96;});
  if(this.motion&&(this.orbit||this.rain||Math.abs(this.targetExplode-this.explode)>.002))this.request();
 }
 setZone(i){this.zone=i;this.request();}
 setMode(mode){this.mode=mode;this.targetExplode=mode==='exploded'?.6:0;this.request();}
 rotate(a){this.yaw+=a;this.orbit=false;this.syncControls();this.request();}
 zoom(direction){this.distance=clamp(this.distance-direction*1.3,12.4,28);this.request();}
 // Default presentation: raining and orbiting, while respecting the global motion preference.
 syncControls(){document.querySelector('[data-rain]')?.setAttribute('aria-pressed',String(this.rain));document.querySelector('[data-orbit]')?.setAttribute('aria-pressed',String(this.orbit));}
 reset(){this.yaw=.61;this.elev=.37;this.distance=21.0;this.mode='cutaway';this.targetExplode=0;this.rain=this.motion;this.orbit=this.motion;document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode==='cutaway')));this.syncControls();this.request();}
 setRain(v){this.rain=Boolean(v&&this.motion);this.syncControls();this.request();}
 setOrbit(v){this.orbit=Boolean(v&&this.motion);this.syncControls();this.request();}
 setMotion(v){const enabling=v&&!this.motion;this.motion=Boolean(v);if(!v){this.rain=false;this.orbit=false;}else if(enabling){this.rain=true;this.orbit=true;}this.syncControls();this.request();}
 setVisible(v){this.visible=v;this.prev=0;if(!v){cancelAnimationFrame(this.raf);this.raf=0;}else this.request();}
 destroy(){if(this.dead)return;this.dead=true;this.abort.abort();this.resizeObserver.disconnect();cancelAnimationFrame(this.raf);if(this.gl){this.gl.deleteBuffer(this.buffer);this.gl.deleteBuffer(this.rainBuffer);this.gl.deleteProgram(this.program);this.gl.getExtension('WEBGL_lose_context')?.loseContext();}this.faces=null;this.pinRoot.innerHTML='';}
}
window.W360House=House;
})();
