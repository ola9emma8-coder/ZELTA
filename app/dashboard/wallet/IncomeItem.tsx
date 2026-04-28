type Props = {
  title: string;
  amount: number;
  icon: React.ReactNode;
};

export default function IncomeItem({ title, amount, icon }: Props) {
  return (
    <div className="flex justify-between items-center p-4 bg-white rounded-xl shadow-sm">
      <div className="flex space-x-2 items-center">
        <span className="rounded-full p-3 bg-transparent">{icon}</span>
        <p>{title}</p>
      </div>
      <p className="font-semibold">₦{amount.toLocaleString()}</p>
    </div>
  );
}
