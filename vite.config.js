import { defineConfig } from 'vite';

export default defineConfig({
  root: import.meta.dirname,
  publicDir: 'public',
  css: {
    postcss: {},  // 不使用父目录的 PostCSS 配置
  },
  build: {
    outDir: 'dist',
    assetsInlineLimit: 0,
  },
});
