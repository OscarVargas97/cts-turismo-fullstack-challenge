<script setup lang="ts">
const route = useRoute();

const token = route.params.token as string | undefined;

const loading = ref(true);
const error = ref(false);
const message = ref("");
const resultUser = ref(null);
const email = ref("-");
const stop_email = ref(false);
const pass_data = ref("");

async function send_email() {
  if (!email.value) {
    stop_email.value = true;
    message.value = "Ya no puedes usar este enlace, revisa tu correo";
    return;
  }
  try {
    const res: ApiResponse = await apiClient("/api/send_email/", {
      method: "POST",
      body: JSON.stringify({ email: email.value }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    message.value = "Correo enviado con nuevo enlace.";
    email.value = "";
  } catch (err: any) {
    console.log(err);
  }
}

async function verify() {
  if (!token) {
    return;
  }

  try {
    const res: ApiResponse = await apiClient("/api/verify/", {
      method: "POST",
      body: JSON.stringify({ token }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    console.log(res);
    pass_data.value = res.data.password_reset_token;
    message.value =
      "Correo verificado con éxito. Por favor, cambie su contraseña.";
  } catch (err: any) {
    email.value = err.errors.detail.email;
    error.value = true;
    error.value = true;
    message.value =
      "Hubo un error al verificar, reenvié el correo, por favor intente de nuevo.";
    resultUser.value = null;
  } finally {
    loading.value = false;
  }
}
onMounted(() => {
  verify();
});
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-200 to-blue-300 p-4"
  >
    <div
      class="bg-white/95 rounded-2xl shadow-xl p-10 max-w-md w-full transform transition-transform hover:scale-105"
    >
      <!-- Carga -->
      <div v-if="loading" class="flex items-center justify-center p-6">
        <svg
          class="animate-spin h-10 w-10 text-blue-500"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
          ></path>
        </svg>
      </div>

      <!-- Mensaje y botones -->
      <div v-else class="flex flex-col gap-6 text-center">
        <h2 class="text-2xl font-bold text-blue-800">Verificación de Correo</h2>

        <p class="text-gray-700">
          {{ message }}
        </p>

        <div class="flex flex-col gap-4">
          <RouterLink
            v-if="!error"
            :to="`/auth/change-password/${pass_data}`"
            class="w-full px-6 py-3 bg-green-500 text-white font-semibold rounded-lg shadow-lg hover:bg-green-600 transition"
          >
            Continuar
          </RouterLink>

          <button
            v-else
            v-if="!stop_email"
            class="w-full px-6 py-3 bg-red-500 text-white font-semibold rounded-lg shadow-lg hover:bg-red-600 transition"
            @click="send_email"
          >
            Reenviar correo
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
