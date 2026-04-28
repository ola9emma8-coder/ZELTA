"use client";
import { useSearchParams } from "next/navigation";
import PageHeader from "@/components/PageHeader";

// import Section from "@/components/Section";
import BiasAlertCard from "@/app/dashboard/BiasAlertCard";
import MarketAlert from "@/app/dashboard/MarketAlert";
import WeeklyVerdictCard from "@/app/dashboard/WeeklyVerdictCard";
import DecisionScoreCard from "./DecisionScoreCard";
import StressIndexCard from "./StressIndexCard";

const time = new Date().toLocaleString("en-US", {
  hour: "numeric",
  minute: "numeric",
  hour12: true,
});

const greeting = time.includes("AM") ? "Good Morning" : "Good evening";

function Dashboard() {
  const searchParam = useSearchParams();
  const name = searchParam.get("username");
  return (
    <section className="space-y-6">
      <PageHeader
        title={`${greeting},\n ${name}`}
        description="here's your financial intelligence for today"
      ></PageHeader>

      <main className="pb-8 space-y-3">
        {/*  DASHBOARD HOMEPAGE WIWDGET 1 */}
        <MarketAlert />
        {/*  DASHBOARD HOMEPAGE WIWDGET 2 */}

        {/*  DASHBOARD HOMEPAGE WIWDGET 3 */}
        <StressIndexCard />

        {/* DASHBOARD HOME WODGET 4 */}
        <BiasAlertCard />

        {/* DASHBOARD HOME 5 */}
        <DecisionScoreCard />

        <WeeklyVerdictCard />
      </main>
    </section>
  );
}

export default Dashboard;
