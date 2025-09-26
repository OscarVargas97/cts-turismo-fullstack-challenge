<script setup lang="ts">
import { navigateTo, useRoute } from "#app";
import { ref, reactive } from "vue";

const route = useRoute();
const token = route.params.token as string | undefined;

const { loggedIn, user, fetch: refreshSession } = useUserSession();

const credentials = reactive({
  password: "",
  confirmPassword: "",
});

const errorMessage = ref("");
const showError = ref(false);

const message = ref("");
const showMessage = ref(false);

async function changePassword() {
  errorMessage.value = "";
  showError.value = false;
  showMessage.value = false;

  // Validar que las contraseñas coincidan
  if (credentials.password !== credentials.confirmPassword) {
    errorMessage.value = "Las contraseñas no coinciden";
    showError.value = true;
    return;
  }

  if (!token) {
    errorMessage.value = "Token inválido o faltante";
    showError.value = true;
    return;
  }

  try {
    await $fetch("/api/change-password", {
      method: "POST",
      body: {
        token,
        password: credentials.password,
      },
    });

    await refreshSession();

    // Mostrar mensaje de éxito
    message.value = "Contraseña cambiada con éxito 🎉. Redirigiendo...";
    showMessage.value = true;

    // Redirigir después de unos segundos
    setTimeout(() => {
      navigateTo("/");
    }, 2500);
  } catch (err: any) {
    console.error(err);
    errorMessage.value = err?.message || "Error al cambiar la contraseña";
    showError.value = true;
  }
}
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-200 to-blue-300 p-4"
  >
    <div
      class="bg-white/95 rounded-2xl shadow-xl p-10 max-w-md w-full transform transition-transform hover:scale-105"
    >
      <h2 class="text-3xl font-extrabold text-blue-800 mb-6 text-center">
        Cambio de Contraseña
      </h2>

      <form
        v-if="!showMessage"
        @submit.prevent="changePassword"
        class="flex flex-col gap-4"
      >
        <input
          v-model="credentials.password"
          type="password"
          placeholder="Nueva contraseña"
          required
          class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-800"
        />

        <input
          v-model="credentials.confirmPassword"
          type="password"
          placeholder="Confirmar nueva contraseña"
          required
          class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-800"
        />

        <button
          type="submit"
          class="w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:bg-blue-700 transition"
        >
          Cambiar contraseña
        </button>

        <p v-if="showError" class="text-red-500 text-sm mt-2">
          {{ errorMessage }}
        </p>
      </form>

      <!-- Mensaje de éxito -->
      <div v-if="showMessage" class="text-center">
        <p class="text-green-600 text-lg font-semibold">{{ message }}</p>
      </div>
    </div>
  </div>
</template>
