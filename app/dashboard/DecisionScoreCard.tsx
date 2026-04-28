import { ArrowDownRight } from "lucide-react";

export default function DecisionScoreCard() {
  return (
    <div className=" p-5 rounded-xl space-y-5">
      <div className="flex justify-between">
        <p className="font-bold uppercase text-sm">Decision Confidence Score</p>
        <ArrowDownRight />
      </div>

      <Bar label="Rational" value={58} color="green" />
      <Bar label="Impulse" value={42} color="orange" />

      <div className="bg-green-50 text-[#444] p-3 rounded-lg text-sm">
        <strong>Confidence Gap: 16%</strong> – Moderate urgency
      </div>
    </div>
  );
}

function Bar({
  label,
  value,
  color,
}: {
  label: string;
  value: number;
  color: "green" | "orange";
}) {
  return (
    <div>
      <div className="flex justify-between text-sm">
        <span>{label}</span>
        <span>{value}%</span>
      </div>

      <div className="w-full bg-gray-100 h-2 rounded-full">
        <div
          className={`h-2 rounded-full bg-${color}-500`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}
