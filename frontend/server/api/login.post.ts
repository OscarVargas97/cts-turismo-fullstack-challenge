import { z } from "zod";

const bodySchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export default defineEventHandler(async (event) => {
  const { email, password } = await readValidatedBody(event, bodySchema.parse);
  const config = useRuntimeConfig(event);

  const backendRes = await fetch(
    `${config.public.BACKEND_URL}/authentication/login/`,
    {
      method: "POST",
      body: JSON.stringify({ email, password }),
      headers: { "Content-Type": "application/json" },
      credentials: "include",
    }
  );

  const rest = await handleApiResponse(backendRes);

  setCookiesFromResponse(event, backendRes);

  const { user } = rest.data || {};
  if (!user?.uuid) {
    throw createError({ statusCode: 401, message: "UUID missing" });
  }

  await setUserSession(event, {
    user: { email: user.email, uuid: user.uuid },
  });
});