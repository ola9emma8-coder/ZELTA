type Status = "on-track" | "watch" | "over";

type Props = {
  name: string;
  used: number;
  total: number;
  status: Status;
};

export default function SpendingCategoryCard({
  name,
  used,
  total,
  status,
}: Props) {
  const progress = (used / total) * 100;
  const statusColor = {
    "on-track": "text-green-600",
    watch: "text-yellow-500",
    over: "text-red-600",
  };

  return (
    <div className="p-4 bg-white rounded-xl shadow-sm space-y-2">
      <div className="flex justify-between">
        <p>{name}</p>
        <p
          className={`text-[12px] font-semibold p-2 rounded-xl border border-gray-50 ${statusColor[status]}`}
        >
          {status.toUpperCase()}
        </p>
      </div>

      <p className="text-sm text-gray-500">
        ₦{used} / ₦{total}
      </p>

      <div className="h-2 bg-gray-200 rounded-full">
        <div
          className="h-2 bg-green-500 rounded-full"
          style={{ width: `${Math.min(progress, 100)}%` }}
        />
      </div>
    </div>
  );
}
