import { Activity } from "lucide-react";

export default function MarketAlert() {
  return (
    <div className="flex items-center gap-3 p-3 rounded-xl bg-orange-50 text-sm">
      <Activity color="orange" size={20} />
      <p className="font-medium">Bayse Market USD/NGN crowd pricing 68% fear</p>
    </div>
  );
}
