if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js?v=20260928-11',{updateViaCache:'none'}).catch(error => console.warn('Falha ao registrar service worker:', error));
      });
    }
