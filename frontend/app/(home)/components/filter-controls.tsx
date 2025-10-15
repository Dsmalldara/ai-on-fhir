import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useQuery } from "@tanstack/react-query";

type FilterOptions = {
  age_ranges?: string[];
  genders?: string[];
  diagnosis_codes?: string[];
};

async function fetchFilterOptions(): Promise<FilterOptions> {
  // Replace with your actual fetch logic
  return {
    age_ranges: ["0-18", "19-35", "36-60", "60+"],
    genders: ["Male", "Female", "Other"],
    diagnosis_codes: ["A01", "B02", "C03"],
  };
}

function FilterControls({
  onFilterChange,
}: {
  onFilterChange: (filterType: string, value: any) => void;
}) {
  const { data: filterOptions, isLoading } = useQuery({
    queryKey: ["filterOptions"],
    queryFn: fetchFilterOptions,
  });

  if (isLoading || !filterOptions) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Additional Filters</CardTitle>
        <CardDescription>Refine your search with these options</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 md:grid-cols-3">
          {filterOptions.age_ranges && (
            <div>
              <label className="text-sm font-medium mb-2 block">
                Age Range
              </label>
              <Select
                onValueChange={(val) => onFilterChange("age_filter", val)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select age range" />
                </SelectTrigger>
                <SelectContent>
                  {filterOptions.age_ranges.map((range) => (
                    <SelectItem key={range} value={range}>
                      {range}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}

          {filterOptions.genders && (
            <div>
              <label className="text-sm font-medium mb-2 block">Gender</label>
              <Select
                onValueChange={(val) => onFilterChange("gender_filter", val)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select gender" />
                </SelectTrigger>
                <SelectContent>
                  {filterOptions.genders.map((gender) => (
                    <SelectItem key={gender} value={gender}>
                      {gender}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}

          {filterOptions.diagnosis_codes && (
            <div>
              <label className="text-sm font-medium mb-2 block">
                Diagnosis
              </label>
              <Select
                onValueChange={(val) => onFilterChange("diagnosis_filter", val)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select diagnosis" />
                </SelectTrigger>
                <SelectContent>
                  {filterOptions.diagnosis_codes.map((code) => (
                    <SelectItem key={code} value={code}>
                      {code}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

export default FilterControls;
