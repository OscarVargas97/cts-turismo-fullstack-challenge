import { z } from "zod";

const bodySchema = z.object({
  token: z.string(),
  password: z.string().min(8, "La contraseña debe tener al menos 8 caracteres"),
});

export default defineEventHandler(async (event) => {
  const { token, password } = await readValidatedBody(event, bodySchema.parse);

  const config = useRuntimeConfig(event);

  console.log("Token recibido:", token);

  const backendRes = await fetch(
    `${config.public.BACKEND_URL}/authentication/change-password/`,
    {
      method: "POST",
      body: JSON.stringify({
        token,
        new_password: password,
        confirm_password: password,
      }),
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    }
  );

  return await handleApiResponse(backendRes);
});
