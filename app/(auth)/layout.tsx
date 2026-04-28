import { AuthProvider } from "@/context/authContext";
import { JSX } from "react";

// const BASE_URL = "https://zelta-backend-990094999937.us-central1.run.app/";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  return (
    <main>
      <AuthProvider>{children}</AuthProvider>;<div></div>
    </main>
  );
}
