type Props = {
  title: string;
  action?: string;
  children: React.ReactNode;
};

export default function Section({ title, action, children }: Props) {
  return (
    <section className="space-y-3">
      <div className="flex justify-between items-center">
        <h2 className="font-semibold text-lg text-[#444]">{title}</h2>
        {action && <button className="text-sm text-green-600">{action}</button>}
      </div>

      <div className="space-y-3">{children}</div>
    </section>
  );
}
