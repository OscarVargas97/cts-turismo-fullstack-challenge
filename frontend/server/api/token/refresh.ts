export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);

  try {
    if (validateAccessToken(event)) {
      return { success: true, message: "Token todavía válido" };
    }

    const backendRes = await fetch(
      `${config.public.BACKEND_URL}/authentication/refresh/`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
      }
    );

    if (!backendRes.ok) {
      throw new Error("No se pudo refrescar el token");
    }

    const rest = await handleApiResponse(backendRes);

    setCookiesFromResponse(event, backendRes);

    const { user } = rest.data || {};
    if (!user?.uuid) {
      throw new Error("UUID missing");
    }

    await setUserSession(event, {
      user: { email: user.email, uuid: user.uuid },
    });

    return { success: true, user };
  } catch (error) {
    console.error("Error refrescando token:", error);

    // Limpiar sesión del usuario
    await deleteUserSession(event);

    throw createError({
      statusCode: 401,
      message: "Sesión inválida o expiró. Por favor, inicia sesión de nuevo.",
    });
  }
});
