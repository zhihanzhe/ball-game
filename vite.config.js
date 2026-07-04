import { defineConfig } from 'vite';

export default defineConfig({
  root: import.meta.dirname,
  publicDir: 'public',
  base: './',
  css: {
    postcss: {},
  },
  build: {
    outDir: 'dist',
    target: 'es2015',  // 兼容微信X5等旧WebView
    assetsInlineLimit: 0,
    rollupOptions: {
      output: {
        format: 'iife',
        inlineDynamicImports: true,
      },
    },
  },
});
