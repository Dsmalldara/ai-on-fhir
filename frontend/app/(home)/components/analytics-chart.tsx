"use client";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { BarChart3, Users } from "lucide-react";
import { useMemo } from "react";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { paths } from "@/src/types/api";

const COLORS = ["#3b82f6", "#ef4444", "#10b981", "#f59e0b"];

type ChartDataResponse =
  paths["/analytics/chart-data"]["get"]["responses"][200]["content"]["application/json"];

interface Props {
  data: ChartDataResponse | undefined;
}

export default function AnalyticsCharts({ data }: Props) {
  const ageData = useMemo(() => {
    if (!data?.age_distribution) return [];
    return data.age_distribution.map((item) => ({
      name: item.age_group,
      value: item.count,
    }));
  }, [data]);

  const genderData = useMemo(() => {
    if (!data?.gender_distribution) return [];
    return data.gender_distribution.map((item) => ({
      name: item.gender,
      value: item.count,
    }));
    console.log(genderData);
  }, [data]);

  if (!data || data.total_patients === 0) return null;

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {/* Age Distribution */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            Age Distribution
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={ageData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Gender Distribution */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Users className="h-5 w-5" />
            Gender Distribution
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={genderData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name}: ${((percent as number) * 100).toFixed(0)}%`
                }
                outerRadius={80}
                dataKey="value"
              >
                {genderData.map((_, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
