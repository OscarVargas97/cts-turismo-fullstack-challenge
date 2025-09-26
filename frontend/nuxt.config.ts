export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  dirs: ["app/utils", "server/utils"],
  runtimeConfig: {
    public: {
      BACKEND_URL: process.env.BACKEND_URL || "http://localhost:8000",
    },
  },
  css: ["@/assets/css/main.css"],
  modules: [
    "@nuxt/eslint",
    "@nuxt/image",
    "@nuxt/scripts",
    "@nuxt/test-utils",
    "@nuxt/ui",
    "nuxt-auth-utils",
  ],
});