(() => {
  const originalFetch = window.fetch.bind(window);
  let token = document.querySelector('meta[name="csrf-token"]')?.content || '';
  window.fetch = async (input, init = {}) => {
    const request = new Request(input, init);
    if (new URL(request.url).origin !== location.origin) return originalFetch(request);
    const headers = new Headers(request.headers);
    headers.set('Accept', request.url.includes('/api/') ? 'application/json' : (headers.get('Accept') || '*/*'));
    if (!['GET', 'HEAD', 'OPTIONS'].includes(request.method)) headers.set('X-CSRF-TOKEN', token);
    const response = await originalFetch(new Request(request, {headers}));
    token = response.headers.get('X-CSRF-TOKEN') || token;
    return response;
  };
})();
