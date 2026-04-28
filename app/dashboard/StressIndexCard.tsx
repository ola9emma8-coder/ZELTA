import { TrendingDown } from "lucide-react";

export default function StressIndexCard() {
  return (
    <div className="bg-white p-5 rounded-xl space-y-5 shadow-sm">
      <div className="flex justify-between items-center">
        <p className="font-bold uppercase text-sm">Student Stress Index</p>

        <span className="p-2 bg-green-100 rounded-lg">
          <TrendingDown color="green" />
        </span>
      </div>

      <h2 className="text-3xl font-bold text-green-500">34/100</h2>

      <span className="bg-green-50 text-green-600 px-3 py-1 rounded-lg text-sm font-medium">
        Calm · Moderate
      </span>

      <div className="p-2">
        <div className="flex justify-between text-sm">
          <span>Bayse Primary Signal</span>
          <span>28%</span>
        </div>

        <progress value={34} max={100} className="w-full h-2 rounded-full" />
      </div>

      <p className="text-sm text-gray-500">
        Nigerian markets are anxious. Your spending may be influenced by fear.
      </p>

      <div className="flex gap-3">
        <MiniStat title="Bayse Crowd" value="68%" color="orange" />
        <MiniStat title="Zelta Model" value="54%" color="green" />
      </div>
    </div>
  );
}

function MiniStat({
  title,
  value,
  color,
}: {
  title: string;
  value: string;
  color: "green" | "orange";
}) {
  return (
    <div className="flex-1 p-3 bg-gray-50 rounded-lg">
      <p className="text-sm">{title}</p>
      <p className={`font-semibold text-${color}-500`}>{value}</p>
    </div>
  );
}
