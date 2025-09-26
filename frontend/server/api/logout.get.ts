// server/api/logout.post.ts

export default defineEventHandler(async (event) => {
  await deleteUserSession(event);

  return {
    success: true,
    message: "Sesión cerrada correctamente",
  };
});
