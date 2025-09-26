export function setCookiesFromResponse(event: H3Event, response: Response) {
  const rawHeaders: any = (response as any).headers?.raw?.() || {};
  const setCookies = rawHeaders["set-cookie"] || [];

  if (Array.isArray(setCookies) && setCookies.length) {
    event.node.res.setHeader("set-cookie", setCookies);
  } else {
    const single = response.headers.get("set-cookie");
    if (single) event.node.res.setHeader("set-cookie", single);
  }
}
