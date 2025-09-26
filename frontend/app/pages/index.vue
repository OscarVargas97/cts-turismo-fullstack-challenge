<script setup lang="ts">
import { navigateTo } from "#app";
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-200 to-blue-300 p-4">
    <div
      class="bg-white/95 rounded-2xl shadow-xl p-10 max-w-md w-full text-center transform transition-transform hover:scale-105"
    >
      <h1 class="text-4xl font-extrabold text-blue-800 mb-4">¡Bienvenido!</h1>
      <p class="text-gray-700 mb-6 text-lg">
        Regístrate para acceder a nuestras funciones y participar en sorteos exclusivos.
      </p>

      <ul class="text-left text-gray-700 mb-8 space-y-3">
        <li class="flex items-center gap-2">
          <span class="text-green-500">✔</span>
          <span>Acceso a sorteos y promociones</span>
        </li>
        <li class="flex items-center gap-2">
          <span class="text-green-500">✔</span>
          <span>Información actualizada</span>
        </li>
        <li class="flex items-center gap-2">
          <span class="text-green-500">✔</span>
          <span>Experiencia personalizada</span>
        </li>
      </ul>

      <NuxtLink
        to="/auth/register"
        class="w-full block px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:bg-blue-700 transition"
      >
        Registrarme al sorteo
      </NuxtLink>
    </div>
  </div>
</template>
