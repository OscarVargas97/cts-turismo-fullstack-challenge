<script setup lang="ts">
definePageMeta({
  middleware: ["authenticated"],
});

import { ref, computed, onMounted, watch } from "vue";

interface Participant {
  id: number;
  name: string;
}

const participants = ref<Participant[]>([]);
const winner = ref<Participant | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);

const currentPage = ref(1);
const itemsPerPage = 5;
const totalPages = ref(1);

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
}

async function selectRandomParticipant() {
  try {
    const res: ApiResponse = await apiClient("/api/get-winner", {
      method: "Get",
      headers: {
        "Content-Type": "application/json",
      },
    });
  } catch (err: any) {}
}

async function fetchParticipants(page: number) {
  loading.value = true;
  error.value = null;

  try {
    const res = await fetch(
      `/api/participants?page=${page}&limit=${itemsPerPage}`
    );
    if (!res.ok) throw new Error("Error fetching participants");

    const data = await res.json();

    participants.value = data.participants;
    totalPages.value = data.totalPages;
  } catch (err: any) {
    error.value = err.message || "Error loading participants";
  } finally {
    loading.value = false;
  }
}

// Llamar cuando la página cambie
watch(currentPage, (newPage) => {
  fetchParticipants(newPage);
});

// Cargar inicial
onMounted(() => {
  fetchParticipants(currentPage.value);
});
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-200 to-blue-300 p-4"
  >
    <div
      class="bg-white/95 rounded-2xl shadow-xl p-10 max-w-md w-full transform transition-transform hover:scale-105 text-center"
    >
      <h2 class="text-3xl font-extrabold text-blue-800 mb-6">
        Panel Admin - Sorteo
      </h2>

      <div class="mb-6">
        <h3 class="text-xl font-semibold text-gray-800 mb-3">Participantes</h3>

        <div v-if="loading" class="text-center p-4">
          Cargando participantes...
        </div>
        <div v-else-if="error" class="text-red-500 p-4">{{ error }}</div>
        <div v-else>
          <div
            class="max-h-48 overflow-y-auto border rounded-lg p-3 bg-gray-50"
          >
            <ul class="text-left text-gray-700 list-disc list-inside space-y-2">
              <li v-for="p in participants" :key="p.id">
                <strong>{{ p.username }}</strong
                ><br />
                Email: {{ p.email }}<br />
                Teléfono: {{ p.phone_number }}<br />
                Registrado: {{ new Date(p.registration_date).toLocaleString() }}
              </li>
            </ul>
          </div>

          <div class="flex justify-center gap-2 mt-3">
            <button
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400 disabled:opacity-50"
            >
              ◀
            </button>

            <span class="px-2 py-1 font-medium">
              Página {{ currentPage }} de {{ totalPages }}
            </span>

            <button
              @click="goToPage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400 disabled:opacity-50"
            >
              ▶
            </button>
          </div>
        </div>
      </div>

      <button
        @click="selectRandomParticipant"
        class="w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:bg-blue-700 transition mb-6"
      >
        Random Select
      </button>

      <div
        v-if="winner"
        class="p-4 bg-green-100 rounded-lg text-green-800 font-bold text-lg"
      >
        Ganador: {{ winner.username }} — {{ winner.email }}
      </div>
    </div>
  </div>
</template>
