"use client";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Filter } from "lucide-react";
import type { paths } from "@/src/types/api";

type QueryResponse =
  paths["/query"]["post"]["responses"][200]["content"]["application/json"];

interface Props {
  parsedFilters: QueryResponse["parsed_filters"];
  appliedFilters: QueryResponse["applied_filters"];
}

export default function FiltersDisplay({
  parsedFilters,
  appliedFilters,
}: Props) {
  const hasFilters =
    appliedFilters.age_filter ||
    appliedFilters.gender_filter ||
    (appliedFilters.diagnosis_filter &&
      appliedFilters.diagnosis_filter.length > 0);

  if (!hasFilters) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg flex items-center gap-2">
          <Filter className="h-5 w-5" />
          Applied Filters
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-2">
          {appliedFilters.age_filter && (
            <Badge variant="secondary">Age: {appliedFilters.age_filter}</Badge>
          )}
          {appliedFilters.gender_filter && (
            <Badge variant="secondary">
              Gender: {appliedFilters.gender_filter}
            </Badge>
          )}
          {appliedFilters.diagnosis_filter &&
            Array.isArray(appliedFilters.diagnosis_filter) &&
            appliedFilters.diagnosis_filter.map((diag) => (
              <Badge key={diag} variant="secondary">
                Diagnosis: {diag}
              </Badge>
            ))}
        </div>
        <p className="text-sm text-muted-foreground mt-4">
          Query: &quot;{parsedFilters.raw_text}&quot;
        </p>
      </CardContent>
    </Card>
  );
}
