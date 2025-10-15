import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { paths } from "@/src/types/api";

// Props type
export type Query =
  paths["/query"]["post"]["responses"][200]["content"]["application/json"];
type Patient = Query["results_sample"][number];

function PatientsTable({
  patients,
  Query,
}: {
  patients: Patient[] | undefined;
  Query: Query;
}) {
  if (!patients || patients.length === 0) {
    return (
      <Card>
        <CardContent className="py-8">
          <p className="text-center text-gray-500">
            No patients found matching your query.
          </p>
        </CardContent>
      </Card>
    );
  }

  // Helper to get formatted fields
  const formatName = (name: Patient["name"]) => {
    const typedName = name as { given: string[]; family: string };
    return `${typedName.given.join(" ")} ${typedName.family}`;
  };

  const calculateAge = (birthDate: string) => {
    const birth = new Date(birthDate);
    const ageDiff = Date.now() - birth.getTime();
    return Math.floor(ageDiff / (1000 * 60 * 60 * 24 * 365.25));
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Patient Results</CardTitle>
        <CardDescription>
          {Query.summary.total_patients_found} patient(s) found
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b">
                <th className="text-left py-2 px-3 font-semibold">Name</th>
                <th className="text-left py-2 px-3 font-semibold">Age</th>
                <th className="text-left py-2 px-3 font-semibold">Gender</th>
                <th className="text-left py-2 px-3 font-semibold">
                  Conditions
                </th>
                <th className="text-left py-2 px-3 font-semibold">
                  Medications
                </th>
              </tr>
            </thead>
            <tbody>
              {patients.map((patient) => (
                <tr
                  key={patient.id as string}
                  className="border-b hover:bg-gray-50"
                >
                  <td className="py-3 px-3">{formatName(patient.name)}</td>
                  <td className="py-3 px-3">
                    {calculateAge(patient.birthDate as string)}
                  </td>
                  <td className="py-3 px-3 capitalize">
                    {patient.gender as string}
                  </td>
                  <td className="py-3 px-3">
                    {Array.isArray(patient.conditions)
                      ? patient.conditions
                          .map((c: { display: string }) => c.display)
                          .join(", ")
                      : "None"}
                  </td>
                  <td className="py-3 px-3">
                    {Array.isArray(patient.medications) &&
                    patient.medications.length > 0
                      ? patient.medications.join(", ")
                      : "None"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}

export default PatientsTable;
