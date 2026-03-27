// Polyfill for process object
if (typeof window !== 'undefined') {
  window.process = {
    env: {
      NODE_ENV: 'development'
    },
    version: '1.0.0',
    platform: 'web'
  };
}

if (typeof global !== 'undefined') {
  global.process = {
    env: {
      NODE_ENV: 'development'
    },
    version: '1.0.0',
    platform: 'web'
  };
}

if (typeof self !== 'undefined') {
  self.process = {
    env: {
      NODE_ENV: 'development'
    },
    version: '1.0.0',
    platform: 'web'
  };
}
