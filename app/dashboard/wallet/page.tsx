"use client";
import React, { useState } from "react";
import PageHeader from "@/components/PageHeader";
import AlertBanner from "./AlertBanner";
import BalanceCard from "./BalanceCard";
import IncomeItem from "./IncomeItem";
import SavingsGoalCard from "./SavingsGoalCard";
import SpendingCategoryCard from "./SpendingCategoryCard";
import Section from "../../../components/Section";
import { Briefcase, Gift, TrendingUp, Eye, EyeClosed } from "lucide-react";
import Button from "@/components/Button";

const incomeSources = [
  {
    id: 1,
    title: "Holiday Job",
    amount: 20000,
    icon: <Briefcase color="green" strokeWidth={1} />,
  },
  {
    id: 2,
    title: "Parents Transfer",
    amount: 15000,
    icon: <Gift className="text-yellow-500" strokeWidth={1} />,
  },
  {
    id: 3,
    title: "Side Hustle",
    amount: 10000,
    icon: <TrendingUp color="green" strokeWidth={1} />,
  },
];

const spending = [
  { id: 1, name: "Food & Data", used: 3500, total: 5000, status: "on-track" },
  { id: 2, name: "Transport", used: 2400, total: 3000, status: "watch" },
  { id: 3, name: "Non-essentials", used: 4200, total: 3000, status: "over" },
];

const goal = {
  title: "Hostel Fee",
  amount: 58500,
  saved: 18500,
  due: "5 weeks",
};
function Page() {
  const [isVisible, setIsVisible] = useState(true);
  return (
    <>
      <PageHeader
        title="ZELTA WALLET"
        description="unified view of your finances"
      >
        <Button className="p-2 mr-4" onClick={() => setIsVisible(!isVisible)}>
          {isVisible ? <Eye /> : <EyeClosed />}
        </Button>
      </PageHeader>
      <main className="p-4 space-y-6">
        {/* Alert Banner */}
        <AlertBanner />

        {/* Balance Card */}
        <BalanceCard total={45000} freeCash={26500} locked={18500} />

        {/* iNCOME SOURCE */}
        <Section title="Income Sources" action="all streams unified">
          {incomeSources.map((souurce) => (
            <IncomeItem key={souurce.id} {...souurce} />
          ))}
        </Section>

        <Section title="Locked Savings Goals" action="Lock New Goal">
          <SavingsGoalCard goal={goal} />
        </Section>

        {/* spending behavior */}
        <Section title="Behavioral Spending Map">
          {spending.map((spending) => (
            <SpendingCategoryCard
              key={spending.id}
              name={spending.name}
              used={spending.used}
              total={spending.total}
              status={spending.status as "on-track" | "watch" | "over"}
            />
          ))}
        </Section>
      </main>
    </>
  );
}

export default Page;
