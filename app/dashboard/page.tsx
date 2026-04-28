import { Suspense } from "react";
import Dashboard from "@/app/dashboard/dashboard";

function Page() {
  return (
    <Suspense fallback={<div>Loading dashboard...</div>}>
      <Dashboard />
    </Suspense>
  );
}

export default Page;
