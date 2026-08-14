/**
 * Centralized API Client & Error Abstraction
 * Handles HTTP requests, base URL resolution, JSON parsing, and unified error handling.
 */

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

// Helper to derive root server URL (for endpoints outside /api/v1 like /health)
const getRootServerUrl = (): string => {
  try {
    const url = new URL(API_BASE_URL);
    return `${url.protocol}//${url.host}`;
  } catch {
    return "http://localhost:8000";
  }
};

export class ApiError extends Error {
  status: number;
  code: string;
  details?: any;

  constructor(status: number, code: string, message: string, details?: any) {
    super(message);
    self.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

export async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = endpoint.startsWith("http")
    ? endpoint
    : `${API_BASE_URL}${endpoint.startsWith("/") ? "" : "/"}${endpoint}`;

  const defaultHeaders: HeadersInit = {
    "Content-Type": "application/json",
    Accept: "application/json",
  };

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    if (!response.ok) {
      let code = "UNKNOWN_ERROR";
      let message = `Request failed with status ${response.status}`;
      let details = null;

      try {
        const errorData = await response.json();
        if (errorData?.error) {
          code = errorData.error.code || code;
          message = errorData.error.message || message;
          details = errorData.error.details || null;
        }
      } catch {
        // Fallback for non-JSON error bodies
      }

      throw new ApiError(response.status, code, message, details);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(
      500,
      "NETWORK_ERROR",
      error instanceof Error ? error.message : "Network error / Backend unreachable"
    );
  }
}

export async function checkBackendHealth(): Promise<{
  online: boolean;
  statusText: string;
}> {
  try {
    const rootUrl = getRootServerUrl();
    const response = await fetch(`${rootUrl}/health`, { cache: "no-store" });
    if (response.ok) {
      const data = await response.json();
      return { online: data?.status === "ok", statusText: data?.status || "ok" };
    }
    return { online: false, statusText: `HTTP ${response.status}` };
  } catch {
    return { online: false, statusText: "Offline / Disconnected" };
  }
}

export const apiClient = {
  get: <T>(endpoint: string, options?: RequestInit) =>
    fetchApi<T>(endpoint, { method: "GET", ...options }),

  post: <T>(endpoint: string, body?: any, options?: RequestInit) =>
    fetchApi<T>(endpoint, {
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
      ...options,
    }),

  put: <T>(endpoint: string, body?: any, options?: RequestInit) =>
    fetchApi<T>(endpoint, {
      method: "PUT",
      body: body ? JSON.stringify(body) : undefined,
      ...options,
    }),

  patch: <T>(endpoint: string, body?: any, options?: RequestInit) =>
    fetchApi<T>(endpoint, {
      method: "PATCH",
      body: body ? JSON.stringify(body) : undefined,
      ...options,
    }),

  delete: <T>(endpoint: string, options?: RequestInit) =>
    fetchApi<T>(endpoint, { method: "DELETE", ...options }),
};
