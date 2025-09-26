<script setup lang="ts">
import { ref, watch, defineProps } from "vue";

const props = defineProps({
  message: String,
  visible: Boolean,
});

const show = ref(props.visible);

watch(
  () => props.visible,
  (val) => {
    show.value = val;

    if (val) {
      setTimeout(() => {
        show.value = false;
      }, 3000); // Ocultar después de 3s
    }
  }
);
</script>

<template>
  <transition name="slide-down">
    <div
      v-if="show"
      class="fixed top-4 left-1/2 transform -translate-x-1/2 bg-red-600 text-white px-6 py-3 rounded-lg shadow-lg z-50"
    >
      {{ message }}
    </div>
  </transition>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}
.slide-down-enter-to {
  transform: translateY(0);
  opacity: 1;
}
.slide-down-leave-from {
  transform: translateY(0);
  opacity: 1;
}
.slide-down-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>
