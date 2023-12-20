import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { readdir, rm, writeFile } from 'fs/promises';

// https://vitejs.dev/config/
export default defineConfig({ 
  build: {
    // sourcemap: 'inline', // enable for debugging
  },
  server: {
    port: 4200,
  },
  plugins: [
    svelte({
      compilerOptions: {
        customElement: true,
      },
  }),
  ]
})
    