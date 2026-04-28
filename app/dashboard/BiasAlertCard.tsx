import { Brain } from "lucide-react";

export default function BiasAlertCard() {
  return (
    <div className="flex gap-4 p-5 bg-orange-50  rounded-xl">
      <Brain color="orange" />

      <div>
        <p className="font-semibold text-sm">Active Bias Detected</p>

        <h2 className="text-xl font-bold text-orange-500 uppercase">
          Loss Aversion
        </h2>

        <p className="text-sm text-gray-600 dark:text-white mt-1">
          Your withdrawal behavior was driven by market panic, not real risk.
        </p>
      </div>
    </div>
  );
}
