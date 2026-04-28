type Props = {
  total: number;
  freeCash: number;
  locked: number;
};
import { Wallet } from "lucide-react";

export default function BalanceCard({ total, freeCash, locked }: Props) {
  return (
    <div className="p-5 rounded-2xl bg-green-500 text-white space-y-4">
      <div className="flex justify-between">
        <div>
          <p className="text-sm opacity-80">Total Balance</p>
          <h1 className="text-3xl lg:text-4xl font-bold">
            ₦{total.toLocaleString()}
          </h1>
        </div>

        <span className="mr-4 rounded-lg">
          <Wallet className="" strokeWidth={1} size={30} />
        </span>
      </div>

      <div className="flex gap-4">
        <div className="bg-white/20 p-3 rounded-xl flex-1">
          <p className="text-sm">Free Cash</p>
          <p className="font-semibold">₦{freeCash.toLocaleString()}</p>
        </div>

        <div className="bg-white/20 p-3 rounded-xl flex-1">
          <p className="text-sm">Locked Goals</p>
          <p className="font-semibold">₦{locked.toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
}
