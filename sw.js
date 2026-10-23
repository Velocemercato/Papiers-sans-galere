// Papiers Sans Galère : pages disponibles même avec une mauvaise connexion.
const CACHE='pp-app-v3';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(['./','./outils.html','./accompagnement.html','./assets/vendor/qrcode.min.js']).catch(()=>{})))});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n.startsWith('pp-app-')&&n!==CACHE).map(n=>caches.delete(n)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;
 const page=r.mode==='navigate',statique=/\.(css|js|webp|png|jpg|jpeg|svg|woff2?)$/.test(new URL(r.url).pathname);
 e.respondWith(fetch(r).then(res=>{if(res.ok&&(page||statique)){const c=res.clone();caches.open(CACHE).then(x=>x.put(r,c))}return res})
 .catch(()=>caches.match(r).then(m=>m||(page?caches.match('./'):new Response('',{status:504,statusText:'Hors connexion'})))))});
