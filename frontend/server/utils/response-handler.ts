export interface ApiResponse<T = any> {
  success: boolean;
  status: number;
  message: string;
  data?: T;
  errors?: Record<string, any>;
}

/**
 * Maneja y normaliza la respuesta del backend.
 * Lanza errores automáticamente cuando la respuesta es incorrecta.
 */
export async function handleApiResponse<T = any>(
  response: Response
): Promise<ApiResponse<T>> {
  let data: any = {};

  try {
    data = await response.json();
  } catch (e) {
    data = {};
  }

  if (!response.ok) {
    throw createError({
      statusCode: response.status || 400,
      statusMessage: data?.message || data?.detail || "Error en la solicitud",
      data: { detail: data?.errors || data?.detail || "Error desconocido" },
    });
  }

  return {
    success: true,
    status: response.status,
    message: data?.message || "Operación exitosa",
    data: data?.data || data,
  };
}
