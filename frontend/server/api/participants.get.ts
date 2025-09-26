export default defineEventHandler(async (event) => {
  const query = getQuery(event);

  const page = query.page || "1";
  const pageSize = query.page_size || "5";

  const config = useRuntimeConfig();
  const API_URL = `${config.public.BACKEND_URL}/raffles/participation/?page=${page}&page_size=${pageSize}`;

  console.log("📌 Endpoint Nuxt /api/participants llamado");
  console.log("🔗 API_URL:", API_URL);
  console.log("📄 Parámetros:", { page, pageSize });

  try {
    const res = await fetch(API_URL);
    if (!res.ok) {
      console.error("❌ Error en fetch:", res.status, res.statusText);
      throw new Error(
        `Error fetching participants from Django API: ${res.statusText}`
      );
    }

    const data = await res.json();

    console.log("📥 Datos recibidos de Django API:", data);

    return {
      participants: data.results || [],
      totalPages:
        data.count && pageSize
          ? Math.ceil(Number(data.count) / Number(pageSize))
          : 1,
    };
  } catch (error: any) {
    console.error("❌ Error en endpoint /api/participants:", error);

    return {
      error: error.message || "Error fetching participants",
      participants: [],
      totalPages: 0,
    };
  }
});
