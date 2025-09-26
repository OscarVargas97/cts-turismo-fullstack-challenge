export async function deleteUserSession(event: any) {
  // Borrar cookies de acceso y refresh
  deleteCookie(event, "access");
  deleteCookie(event, "refresh");
}
