export default function AlertBanner() {
  return (
    <div className="p-4 rounded-xl bg-yellow-50 border border-yellow-200">
      <p className="font-medium text-sm">BQ Alert: Stress-Spending Detected</p>
      <p className="text-sm text-gray-600 mt-1">
        You spent ₦2,400 above normal. ZELTA recommends
        <span className="text-orange-500 font-medium"> HOLD </span>
        non-essential spending this week.
      </p>
    </div>
  );
}
