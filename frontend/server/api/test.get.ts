export default defineEventHandler(async (event) => {
  try {
    const config = useRuntimeConfig(event);

    // Capturar cookies enviadas desde el navegador
    const cookieHeader = event.node.req.headers.cookie || "";

    const res = await $fetch(`${config.public.BACKEND_URL}/raffles/test/`, {
      method: "GET",
      headers: {
        cookie: cookieHeader, // 🔹 reenviar cookies al backend
      },
    });

    return { message: res };
  } catch (err: any) {
    console.error("API Test error:", err);
    throw createError({
      statusCode: err?.status || 500,
      message: err?.message || "Error en API Test",
    });
  }
});
