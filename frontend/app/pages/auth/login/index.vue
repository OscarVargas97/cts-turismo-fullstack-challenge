<script setup lang="ts">
definePageMeta({
  middleware: ["not-authenticated"],
});
const { loggedIn, user, fetch: refreshSession } = useUserSession();

const credentials = reactive({
  email: "",
  password: "",
});

// Usamos estado global para mensajes de error
const errorMessage = useState<string>("errorMessage");
const showError = useState<boolean>("showError");

async function login() {
  errorMessage.value = "";
  showError.value = false;

  try {
    const res: ApiResponse = await apiClient("/api/login", {
      method: "POST",
      body: JSON.stringify(credentials),
      headers: {
        "Content-Type": "application/json",
      },
    });

    await refreshSession();
    await navigateTo("/dashboard");
  } catch (err: any) {
    console.error("Login error:", err);
    errorMessage.value =
      "No se pudo iniciar sesión. Verifica tus credenciales, revisa el correo en caso de que no haya sido verificado o intenta más tarde.";
    showError.value = true;
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-200 to-blue-300 p-4">
    <div class="bg-white/95 rounded-2xl shadow-xl p-10 max-w-md w-full transform transition-transform hover:scale-105">
      <h2 class="text-3xl font-extrabold text-blue-800 mb-6 text-center">Iniciar Sesión</h2>

      <form @submit.prevent="login" class="flex flex-col gap-4">
        <input
          v-model="credentials.email"
          type="email"
          placeholder="Correo electrónico"
          required
          class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-800"
        />

        <input
          v-model="credentials.password"
          type="password"
          placeholder="Contraseña"
          required
          class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-800"
        />

        <button
          type="submit"
          class="w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:bg-blue-700 transition"
        >
          Iniciar Sesión
        </button>
      </form>
    </div>
  </div>
</template>
