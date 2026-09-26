const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

function getToken(): string | null {
  return localStorage.getItem("bjjvault_token");
}

export function setToken(token: string) {
  localStorage.setItem("bjjvault_token", token);
}

export function clearToken() {
  localStorage.removeItem("bjjvault_token");
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });

  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(body.detail ?? "Request failed");
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export function googleLoginUrl(): string {
  return `${API_BASE_URL}/auth/google/login`;
}

export { API_BASE_URL };
