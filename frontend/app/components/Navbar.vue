<script setup lang="ts">
const { loggedIn, clear: clearSession } = useUserSession();

function navigateToLogin() {
  navigateTo("/auth/login"); // SPA
}

function goHome() {
  navigateTo("/"); // SPA
}

async function handleLogout() {
  try {
    await apiClient("/api/logout", {
      method: "GET",
      credentials: "include", // importante si usas cookies
    });

    clearSession(); // Limpia el estado local
    navigateTo("/"); // Redirige al inicio
  } catch (error) {
    console.error("Error cerrando sesión:", error);
  }
}
</script>

<template>
  <nav class="bg-white shadow-md fixed top-0 left-0 w-full z-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <div class="flex-shrink-0 cursor-pointer" @click="goHome">
          <span class="font-bold text-xl text-blue-800">MiApp</span>
        </div>
        <div>
          <button
            v-if="!loggedIn"
            @click="navigateToLogin"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Iniciar Sesión
          </button>

          <button
            v-else
            @click="handleLogout"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>
