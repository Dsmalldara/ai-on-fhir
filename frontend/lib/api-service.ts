import type { paths } from "@/src/types/api";
import { API_BASE_URL } from "./constant";

//  type helpers to extract from OpenAPI paths
type ApiResponse<T> = T extends {
  responses: { 200: { content: { "application/json": infer R } } };
}
  ? R
  : never;

type ApiRequest<T> = T extends {
  requestBody: { content: { "application/json": infer B } };
}
  ? B
  : never;

export type ApiParams<T> = T extends { parameters: { query?: infer Q } }
  ? Q
  : never;

// Generic fetch wrapper
async function fetchApi<P extends keyof paths, M extends keyof paths[P]>(
  path: P,
  method: M,
  init?: {
    body?: ApiRequest<paths[P][M]>;
    params?: ApiParams<paths[P][M]>;
  },
): Promise<ApiResponse<paths[P][M]>> {
  const query = init?.params
    ? "?" +
      new URLSearchParams(
        Object.entries(init.params)
          .filter(([_, v]) => v != null)
          .map(([k, v]) => [k, String(v)]),
      )
    : "";

  const res = await fetch(`${API_BASE_URL}${path}${query}`, {
    method: String(method).toUpperCase(),
    headers: init?.body ? { "Content-Type": "application/json" } : undefined,
    body: init?.body ? JSON.stringify(init.body) : undefined,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail);
  }

  return res.json();
}

// Typed API methods
export const api = {
  health: () => fetchApi("/health", "get"),

  query: (body: ApiRequest<paths["/query"]["post"]>) =>
    fetchApi("/query", "post", { body }),

  suggestions: (params?: ApiParams<paths["/suggestions"]["get"]>) =>
    fetchApi("/suggestions", "get", { params }),

  chartData: (params?: ApiParams<paths["/analytics/chart-data"]["get"]>) =>
    fetchApi("/analytics/chart-data", "get", { params }),

  searchPatients: (params?: ApiParams<paths["/patients/search"]["get"]>) =>
    fetchApi("/patients/search", "get", { params }),

  filterOptions: () => fetchApi("/filters/options", "get"),
};

// Re-export types from OpenAPI (optional, for convenience)
export type {
  ApiResponse as Response,
  ApiRequest as Request,
  ApiParams as Params,
};
