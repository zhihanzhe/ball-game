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
    assetsInlineLimit: 0,
    rollupOptions: {
      output: {
        format: 'iife',
        inlineDynamicImports: true,
      },
    },
  },
});
