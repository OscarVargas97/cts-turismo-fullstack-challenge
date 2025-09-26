<script setup lang="ts">
import Navbar from "~/components/Navbar.vue";

const errorMessage = useState<string>("errorMessage");
const showError = useState<boolean>("showError");

watch(showError, (val) => {
  if (val) {
    setTimeout(() => {
      showError.value = false;
      errorMessage.value = "";
    }, 5000);
  }
});
</script>

<template>
  <div class="relative h-screen flex flex-col">
    <!-- Navbar -->
    <Navbar />

    <!-- Error Popup -->
    <ErrorPopup :message="errorMessage" :visible="showError" />

    <!-- Contenido -->
    <main
      class="overflow-auto flex-1"
      :style="{ minHeight: 'calc(100vh - 4rem)' }"
    >
      <NuxtPage />
    </main>
  </div>
</template>
