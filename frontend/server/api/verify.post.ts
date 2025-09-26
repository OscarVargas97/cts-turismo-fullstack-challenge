import { z } from "zod";

const bodySchema = z.object({
  token: z.string(),
});

export default defineEventHandler(async (event) => {
  const { token } = await readValidatedBody(event, bodySchema.parse);
  const config = useRuntimeConfig(event);
  console.log(token);
  const backendRes = await fetch(
    `${config.public.BACKEND_URL}/authentication/verify-email/`,
    {
      method: "POST",
      body: JSON.stringify({ token }),
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    }
  );

  return await handleApiResponse(backendRes);
});
