"use client";

import { AlertCircle, Loader2 } from "lucide-react";
import { useState } from "react";
import { useDebounce } from "use-debounce";
import AnalyticsCharts from "./analytics-chart";
import FilterControls from "./filter-controls";
import FiltersDisplay from "./filter-display";
import PatientsTable, { Query } from "./patients-table";
import QueryInput from "./query-input";
import ResultsSummary from "./result-summary";
import { useChartData, useSubmitQuery, useSuggestions } from "@/lib/hooks";
import { Alert, AlertDescription } from "@/components/ui/alert";

type AppliedFilters = {
  age_filter?: string | null;
  gender_filter?: string | null;
  diagnosis_filter?: string[] | null;
};

function HomePage() {
  const [queryText, setQueryText] = useState("");
  const [debouncedQuery] = useDebounce(queryText, 300);
  const [appliedFilters, setAppliedFilters] = useState<AppliedFilters>({});

  // Queries
  const { data: suggestions, isLoading: suggestionsLoading } =
    useSuggestions(debouncedQuery);

  // Mutations
  const submitQueryMutation = useSubmitQuery();

  // Use applied filters from backend response if available, otherwise use local state
  const effectiveFilters =
    submitQueryMutation.data?.applied_filters || appliedFilters;
  // Convert diagnosis_filter to string if it's an array
  const chartFilters = {
    ...effectiveFilters,
    diagnosis_filter: Array.isArray(effectiveFilters.diagnosis_filter)
      ? effectiveFilters.diagnosis_filter.join(",")
      : effectiveFilters.diagnosis_filter,
  };
  const { data: chartData } = useChartData(chartFilters);

  const handleSubmit = () => {
    if (!queryText.trim()) return;

    // Pass both query and current filters to backend
    submitQueryMutation.mutate(
      { query: queryText, filters: appliedFilters },
      {
        onSuccess: (data) => {
          // Update local state with filters returned from backend
          if (data.applied_filters) {
            setAppliedFilters(data.applied_filters);
          }
        },
        onError: (error) => {
          console.error("Error:", error);
        },
      },
    );
  };

  const handleFilterChange = (filterType: string, value: any) => {
    setAppliedFilters((prev) => {
      const updated = { ...prev, [filterType]: value };
      console.log("Filters updated:", updated);
      return updated;
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI on FHIR Query Interface
          </h1>
          <p className="text-gray-600">
            Search patient records using natural language queries
          </p>
        </header>

        <div className="space-y-6">
          <QueryInput
            value={queryText}
            onChange={setQueryText}
            onSubmit={handleSubmit}
            suggestions={suggestions?.suggestions}
            loading={suggestionsLoading}
          />

          <FilterControls onFilterChange={handleFilterChange} />

          {submitQueryMutation.isError && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                {(submitQueryMutation.error as Error)?.message ||
                  "Failed to process query. Please check your backend connection."}
              </AlertDescription>
            </Alert>
          )}

          {submitQueryMutation.isPending && (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
              <span className="ml-3 text-gray-600">
                Processing your query...
              </span>
            </div>
          )}

          {submitQueryMutation.isSuccess && submitQueryMutation.data && (
            <>
              <ResultsSummary data={submitQueryMutation.data} />
              <FiltersDisplay
                parsedFilters={submitQueryMutation.data.parsed_filters}
                appliedFilters={submitQueryMutation.data.applied_filters}
              />
              <AnalyticsCharts data={chartData} />
              <PatientsTable
                patients={
                  submitQueryMutation.data.results_sample as {
                    [key: string]: unknown;
                  }[]
                }
                Query={submitQueryMutation.data as Query}
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default HomePage;
