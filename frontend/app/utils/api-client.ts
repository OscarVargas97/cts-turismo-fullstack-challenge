// ~/utils/api-client.ts
export interface ApiResponse<T = any> {
  success: boolean;
  status: number;
  message: string;
  data?: T;
  errors?: Record<string, any>;
}

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
    throw {
      status: response.status || 400,
      message: data?.message || data?.detail || "Error en la solicitud",
      errors: data?.detail || data?.data || data?.data?.error  ||"Error desconocido",
    };
  }

  return {
    success: true,
    status: response.status,
    message: data?.message || "Operación exitosa",
    data: data?.data || data,
  };
}

export async function apiClient<T = any>(
  url: string,
  options: RequestInit
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(url, options);
    return await handleApiResponse<T>(response);
  } catch (err: any) {

    throw {
      status: err?.status || 500,
      message: err?.message || "Error desconocido",
      errors: err?.errors || null,
    };
  }
}
