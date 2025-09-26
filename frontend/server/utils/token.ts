import { jwtDecode } from "jwt-decode";

interface JWTPayload {
  exp?: number;
  [key: string]: any;
}

export function validateAccessToken(
  event: H3Event,
  cookieName = "access"
): boolean {
  const token = getCookieValue(event, cookieName);
  if (!token) return false;

  try {
    const payload: JWTPayload = jwtDecode(token);

    if (!payload.exp) return false;

    const now = Math.floor(Date.now() / 1000);
    return payload.exp > now;
  } catch (error) {
    console.log("Error validando token:", error);
    return false;
  }
}
