import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import type { paths } from "@/src/types/api";
import { api, type ApiParams } from "./api-service";

// Query keys factory
export const keys = {
  suggestions: (q: string) => ["suggestions", q] as const,
  chartData: (filters?: Record<string, any>) => ["chartData", filters] as const,
  filterOptions: () => ["filterOptions"] as const,
  searchPatients: (params?: Record<string, any>) =>
    ["patients", params] as const,
};

// Suggestions hook
export const useSuggestions = (q?: string) =>
  useQuery({
    queryKey: keys.suggestions(q ?? ""),
    queryFn: () => api.suggestions(q ? { q } : undefined),
    enabled: !!q && q.length >= 2,
    staleTime: 5 * 60 * 1000,
  });

export const useSubmitQuery = () => {
  const client = useQueryClient();

  return useMutation({
    mutationFn: ({
      query,
      filters,
    }: {
      query: string;
      filters?: {
        age_filter?: string | null;
        gender_filter?: string | null;
        diagnosis_filter?: string[] | null;
      };
    }) => {
      console.log("Submitting query with filters:", { query, filters });
      return api.query({ query, ...(filters ? { filters } : {}) });
    },
    onSuccess: (data) => {
      console.log("Query successful, returned data:", data);
      client.invalidateQueries({ queryKey: keys.chartData() });
    },
  });
};

// Chart data hook
export const useChartData = (
  filters?: ApiParams<paths["/analytics/chart-data"]["get"]>,
) =>
  useQuery({
    queryKey: keys.chartData(filters),
    queryFn: () => api.chartData(filters),
    staleTime: 10 * 60 * 1000,
  });

// Filter options hook
export const useFilterOptions = () =>
  useQuery({
    queryKey: keys.filterOptions(),
    queryFn: () => api.filterOptions(),
    staleTime: 30 * 60 * 1000,
  });

// Search patients hook
export const useSearchPatients = (
  params?: ApiParams<paths["/patients/search"]["get"]>,
) =>
  useQuery({
    queryKey: keys.searchPatients(params),
    queryFn: () => api.searchPatients(params),
    enabled: !!params,
  });
