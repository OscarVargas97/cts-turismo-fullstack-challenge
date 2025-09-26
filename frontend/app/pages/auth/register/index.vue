<script setup lang="ts">
const registerData = reactive({
  fullName: "",
  email: "",
  phone: "",
});

const errorMessage = useState<string>("errorMessage");
const showError = useState<boolean>("showError");
const isComplete = ref(false); 

async function register() {
  errorMessage.value = "";
  showError.value = false;

  try {
    const res: ApiResponse = await apiClient("/api/register", {
      method: "POST",
      body: JSON.stringify(registerData),
      headers: {
        "Content-Type": "application/json",
      },
    });
    isComplete.value = true;

  } catch (err: any) {


    errorMessage.value =
      err?.message || "Error desconocido en el registro";
    showError.value = true;
  }
}

function goHome() {
  navigateTo("/");
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-200 to-blue-300 p-4">
    <div v-if="!isComplete" class="bg-white/95 rounded-2xl shadow-xl p-10 max-w-md w-full transform transition-transform hover:scale-105">
      
      <h2 class="text-3xl font-extrabold text-blue-800 mb-6 text-center">Registrarme al Sorteo</h2>

      <form @submit.prevent="register" class="flex flex-col gap-4">
        <input
          v-model="registerData.fullName"
          type="text"
          placeholder="Nombre completo"
          required
          class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-800"
        />

        <input
          v-model="registerData.email"
          type="email"
          placeholder="Correo electrónico"
          required
          class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-800"
        />

        <input
          v-model="registerData.phone"
          type="tel"
          placeholder="Teléfono"
          required
          class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white text-gray-800"
        />

        <button
          type="submit"
          class="w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:bg-blue-700 transition"
        >
          Registrar
        </button>
      </form>
    </div>
    <div v-if="isComplete" class="bg-white/95 rounded-2xl shadow-xl p-10 max-w-md w-full transform transition-transform hover:scale-105 text-center">
  <svg class="mx-auto mb-4 w-16 h-16 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
  </svg>
  <h2 class="text-2xl font-bold text-gray-800 mb-2">¡Correo enviado!</h2>
  <p class="text-gray-600 mb-6">
    Hemos enviado un correo a tu dirección con las instrucciones necesarias.<br>
    Revisa tu bandeja de entrada y también la carpeta de spam.
  </p>
<button @click="goHome" class="px-6 py-2 bg-green-500 text-white rounded-full hover:bg-green-600 transition">
  Volver al inicio
</button>
</div>
  </div>
</template>
