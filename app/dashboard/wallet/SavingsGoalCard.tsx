type Goal = {
  title: string;
  amount: number;
  saved: number;
  due: string;
};

export default function SavingsGoalCard({ goal }: { goal: Goal }) {
  const progress = (goal.saved / goal.amount) * 100;

  return (
    <div className="p-4 rounded-xl bg-orange-50 border border-orange-200 space-y-3">
      <div className="flex justify-between">
        <div>
          <p className="font-medium">{goal.title}</p>
          <p className="text-sm text-gray-500">Due in {goal.due}</p>
        </div>

        <p className="font-bold text-orange-600">
          ₦{goal.amount.toLocaleString()}
        </p>
      </div>

      <div className="h-2 bg-gray-200 rounded-full">
        <div
          className="h-2 bg-green-500 rounded-full"
          style={{ width: `${progress}%` }}
        />
      </div>

      <p className="text-sm text-gray-600">
        ₦{goal.saved} / ₦{goal.amount}
      </p>
    </div>
  );
}
