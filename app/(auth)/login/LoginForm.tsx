"use client";
import { useRouter } from "next/navigation";
import Button from "@/components/Button";

interface Props {
  email: string;
  setEmail: React.Dispatch<React.SetStateAction<string>>;
  password: string;
  setPassword: React.Dispatch<React.SetStateAction<string>>;
  handleLogin: (event: React.FormEvent<HTMLFormElement>) => Promise<void>;
  authenticationError: string | null;
}

export default function LoginForm({
  email,
  setEmail,
  password,
  setPassword,
  handleLogin,
  authenticationError,
}: Props) {
  const navigate = useRouter();
  return (
    <section className=" w-full md:w-[50%] lg:w-[40%] xl:w-[25%] mx-auto p-6 rounded-xl flex flex-col justify-center items-between  pt-2 ">
      <h1 className="text-[22px] font-semibold mb-4 text-center ">
        Welcome Back!
      </h1>

      <form
        className="space-y-4 flex flex-col justify-center "
        onSubmit={handleLogin}
      >
        <label className="block text-md font-medium">
          Email
          <input
            type="email"
            value={email}
            onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
              setEmail(event.target.value)
            }
            className=" w-full mt-1 block rounded-lg border border-gray-300 px-8 py-1.5 focus:border-green-500 focus:outline-none"
            placeholder="you@gmail.com"
          />
        </label>

        <label className="block text-md font-medium">
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className="w-full mt-1 block rounded-lg text-start border border-gray-300 px-8 py-1.5 focus:border-green-500 focus:outline-none"
            placeholder="Enter your password"
          />
        </label>

        {authenticationError && (
          <div className="error-message">
            <p className="text-red-500 text-center text-[14px]">
              {authenticationError}
            </p>
          </div>
        )}

        <Button
          // type="submit"
          className="rounded-xl bg-[#10b981] text-white px-6 py-2 hover:bg-[#0b825a]"
        >
          Continue
        </Button>

        <div className="text-center">
          <p>
            New ?{" "}
            <Button
              className="text-green-600"
              onClick={() => {
                navigate.push("/sign-up");
              }}
            >
              Sign up{" "}
            </Button>
          </p>
        </div>
      </form>
    </section>
  );
}
