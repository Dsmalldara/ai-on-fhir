"use client";
import { Card, CardContent } from "@/components/ui/card";
import { Users, TrendingUp } from "lucide-react";
import type { paths } from "@/src/types/api";

type QueryResponse =
  paths["/query"]["post"]["responses"][200]["content"]["application/json"];

interface Props {
  data: QueryResponse;
}

export default function ResultsSummary({ data }: Props) {
  const { summary } = data;
  const confidencePercent = (summary.confidence_score * 100).toFixed(0);
  const confidenceColor =
    summary.confidence_score >= 0.8
      ? "text-green-600"
      : summary.confidence_score >= 0.6
        ? "text-yellow-600"
        : "text-red-600";

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                Patients Found
              </p>
              <p className="text-3xl font-bold">
                {summary.total_patients_found}
              </p>
            </div>
            <Users className="h-8 w-8 text-muted-foreground" />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-muted-foreground">
                Confidence Score
              </p>
              <p className={`text-3xl font-bold ${confidenceColor}`}>
                {confidencePercent}%
              </p>
            </div>
            <TrendingUp className="h-8 w-8 text-muted-foreground" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
