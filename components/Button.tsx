import React from "react";

function Button({
  children,
  onClick,
  className,
}: {
  children: React.ReactNode;
  onClick?: () => void;
  className: string;
  // type: string | null;
}) {
  return (
    <button
      type="submit"
      onClick={onClick}
      className={`cursor-pointer ${className}`}
    >
      {children}
    </button>
  );
}

export default Button;
