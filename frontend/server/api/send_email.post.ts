import { z } from "zod";

const bodySchema = z.object({
  email: z.string(),
});

export default defineEventHandler(async (event) => {
  const { email } = await readValidatedBody(event, bodySchema.parse);
  const config = useRuntimeConfig(event);
  const backendRes = await fetch(
    `${config.public.BACKEND_URL}/authentication/send-verify-email/`,
    {
      method: "POST",
      body: JSON.stringify({ email }),
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    }
  );

  return await handleApiResponse(backendRes);
});
