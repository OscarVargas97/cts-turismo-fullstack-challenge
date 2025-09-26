export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);

  const backendRes = await fetch(
    `${config.public.BACKEND_URL}/authentication/get-winner/`,
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
