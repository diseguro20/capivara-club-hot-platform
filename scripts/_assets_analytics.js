window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
let analyticsReferrer = '';
try { const ref = new URL(document.referrer); analyticsReferrer = ref.origin + ref.pathname; } catch {}
gtag('config', 'G-GZLB9LE37X', {
  page_location: location.origin + location.pathname.replace(/\/checkout\/recuperar\/[^/]+/, '/checkout/recuperar'),
  page_referrer: analyticsReferrer
});
