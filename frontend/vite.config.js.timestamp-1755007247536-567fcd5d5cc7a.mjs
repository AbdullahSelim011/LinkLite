// vite.config.js
import path from "node:path";
import vue from "file:///home/frappe/frappe-bench/apps/linklite/frontend/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import frappeui from "file:///home/frappe/frappe-bench/apps/linklite/frontend/node_modules/frappe-ui/vite/index.js";
import { defineConfig } from "file:///home/frappe/frappe-bench/apps/linklite/frontend/node_modules/vite/dist/node/index.js";
var __vite_injected_original_dirname = "/home/frappe/frappe-bench/apps/linklite/frontend";
var vite_config_default = defineConfig({
  plugins: [
    frappeui({
      frappeProxy: true,
      jinjaBootData: true,
      lucideIcons: true,
      buildConfig: {
        indexHtmlPath: "../linklite/www/links.html",
        emptyOutDir: true,
        sourcemap: true
      }
    }),
    vue()
  ],
  build: {
    chunkSizeWarningLimit: 1500,
    outDir: "../linklite/public/frontend",
    emptyOutDir: true,
    target: "es2015",
    sourcemap: true
  },
  resolve: {
    alias: {
      "@": path.resolve(__vite_injected_original_dirname, "src"),
      "tailwind.config.js": path.resolve(__vite_injected_original_dirname, "tailwind.config.js")
    }
  },
  optimizeDeps: {
    include: ["feather-icons", "showdown", "highlight.js/lib/core", "interactjs"]
  },
  server: {
    allowedHosts: true
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvaG9tZS9mcmFwcGUvZnJhcHBlLWJlbmNoL2FwcHMvbGlua2xpdGUvZnJvbnRlbmRcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIi9ob21lL2ZyYXBwZS9mcmFwcGUtYmVuY2gvYXBwcy9saW5rbGl0ZS9mcm9udGVuZC92aXRlLmNvbmZpZy5qc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vaG9tZS9mcmFwcGUvZnJhcHBlLWJlbmNoL2FwcHMvbGlua2xpdGUvZnJvbnRlbmQvdml0ZS5jb25maWcuanNcIjtpbXBvcnQgcGF0aCBmcm9tIFwibm9kZTpwYXRoXCJcbmltcG9ydCB2dWUgZnJvbSBcIkB2aXRlanMvcGx1Z2luLXZ1ZVwiXG5pbXBvcnQgZnJhcHBldWkgZnJvbSBcImZyYXBwZS11aS92aXRlXCJcbmltcG9ydCB7IGRlZmluZUNvbmZpZyB9IGZyb20gXCJ2aXRlXCJcblxuLy8gaHR0cHM6Ly92aXRlanMuZGV2L2NvbmZpZy9cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyh7XG5cdHBsdWdpbnM6IFtcblx0XHRmcmFwcGV1aSh7XG5cdFx0XHRmcmFwcGVQcm94eTogdHJ1ZSxcblx0XHRcdGppbmphQm9vdERhdGE6IHRydWUsXG5cdFx0XHRsdWNpZGVJY29uczogdHJ1ZSxcblx0XHRcdGJ1aWxkQ29uZmlnOiB7XG5cdFx0XHRcdGluZGV4SHRtbFBhdGg6IFwiLi4vbGlua2xpdGUvd3d3L2xpbmtzLmh0bWxcIixcblx0XHRcdFx0ZW1wdHlPdXREaXI6IHRydWUsXG5cdFx0XHRcdHNvdXJjZW1hcDogdHJ1ZSxcblx0XHRcdH0sXG5cdFx0fSksXG5cdFx0dnVlKCksXG5cdF0sXG5cdGJ1aWxkOiB7XG5cdFx0Y2h1bmtTaXplV2FybmluZ0xpbWl0OiAxNTAwLFxuXHRcdG91dERpcjogXCIuLi9saW5rbGl0ZS9wdWJsaWMvZnJvbnRlbmRcIixcblx0XHRlbXB0eU91dERpcjogdHJ1ZSxcblx0XHR0YXJnZXQ6IFwiZXMyMDE1XCIsXG5cdFx0c291cmNlbWFwOiB0cnVlLFxuXHR9LFxuXHRyZXNvbHZlOiB7XG5cdFx0YWxpYXM6IHtcblx0XHRcdFwiQFwiOiBwYXRoLnJlc29sdmUoX19kaXJuYW1lLCBcInNyY1wiKSxcblx0XHRcdFwidGFpbHdpbmQuY29uZmlnLmpzXCI6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsIFwidGFpbHdpbmQuY29uZmlnLmpzXCIpLFxuXHRcdH0sXG5cdH0sXG5cdG9wdGltaXplRGVwczoge1xuXHRcdGluY2x1ZGU6IFtcImZlYXRoZXItaWNvbnNcIiwgXCJzaG93ZG93blwiLCBcImhpZ2hsaWdodC5qcy9saWIvY29yZVwiLCBcImludGVyYWN0anNcIl0sXG5cdH0sXG5cdHNlcnZlcjoge1xuXHRcdGFsbG93ZWRIb3N0czogdHJ1ZSxcblx0fSxcbn0pXG4iXSwKICAibWFwcGluZ3MiOiAiO0FBQWtVLE9BQU8sVUFBVTtBQUNuVixPQUFPLFNBQVM7QUFDaEIsT0FBTyxjQUFjO0FBQ3JCLFNBQVMsb0JBQW9CO0FBSDdCLElBQU0sbUNBQW1DO0FBTXpDLElBQU8sc0JBQVEsYUFBYTtBQUFBLEVBQzNCLFNBQVM7QUFBQSxJQUNSLFNBQVM7QUFBQSxNQUNSLGFBQWE7QUFBQSxNQUNiLGVBQWU7QUFBQSxNQUNmLGFBQWE7QUFBQSxNQUNiLGFBQWE7QUFBQSxRQUNaLGVBQWU7QUFBQSxRQUNmLGFBQWE7QUFBQSxRQUNiLFdBQVc7QUFBQSxNQUNaO0FBQUEsSUFDRCxDQUFDO0FBQUEsSUFDRCxJQUFJO0FBQUEsRUFDTDtBQUFBLEVBQ0EsT0FBTztBQUFBLElBQ04sdUJBQXVCO0FBQUEsSUFDdkIsUUFBUTtBQUFBLElBQ1IsYUFBYTtBQUFBLElBQ2IsUUFBUTtBQUFBLElBQ1IsV0FBVztBQUFBLEVBQ1o7QUFBQSxFQUNBLFNBQVM7QUFBQSxJQUNSLE9BQU87QUFBQSxNQUNOLEtBQUssS0FBSyxRQUFRLGtDQUFXLEtBQUs7QUFBQSxNQUNsQyxzQkFBc0IsS0FBSyxRQUFRLGtDQUFXLG9CQUFvQjtBQUFBLElBQ25FO0FBQUEsRUFDRDtBQUFBLEVBQ0EsY0FBYztBQUFBLElBQ2IsU0FBUyxDQUFDLGlCQUFpQixZQUFZLHlCQUF5QixZQUFZO0FBQUEsRUFDN0U7QUFBQSxFQUNBLFFBQVE7QUFBQSxJQUNQLGNBQWM7QUFBQSxFQUNmO0FBQ0QsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
