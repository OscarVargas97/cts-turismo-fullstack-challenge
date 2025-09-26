import { z } from "zod";

const bodySchema = z.object({
  fullName: z.string().min(1, "El nombre completo es obligatorio"),
  email: z.string().email("Correo inválido"),
  phone: z.string().min(7, "Teléfono inválido"),
});

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);

  const { fullName, email, phone } = await readValidatedBody(
    event,
    bodySchema.parse
  );

  const backendRes = await fetch(
    `${config.public.BACKEND_URL}/authentication/register/`,
    {
      method: "POST",
      body: JSON.stringify({
        username: fullName,
        email,
        phone_number: phone,
      }),
      headers: { "Content-Type": "application/json" },
    }
  );
  return await handleApiResponse(backendRes);
});
