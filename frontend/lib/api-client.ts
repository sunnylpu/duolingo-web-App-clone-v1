/**
 * Centralized API Client for backend communication.
 * Uses NEXT_PUBLIC_API_URL environment configuration.
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

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

export async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const url = endpoint.startsWith("http")
      ? endpoint
      : `${API_BASE_URL}${endpoint.startsWith("/") ? "" : "/"}${endpoint}`;

    const defaultHeaders: HeadersInit = {
      "Content-Type": "application/json",
    };

    const response = await fetch(url, {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return {
        status: response.status,
        error: errorData?.error?.message || `HTTP Error ${response.status}`,
      };
    }

    const data = await response.json();
    return {
      status: response.status,
      data,
    };
  } catch (err) {
    return {
      status: 500,
      error: err instanceof Error ? err.message : "Network error",
    };
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
  } catch (err) {
    return { online: false, statusText: "Offline / Disconnected" };
  }
}
