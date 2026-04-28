"use client";
import { createContext, useContext, useState } from "react";
import { auth } from "../firebase/index";
import {
  useAuthState,
  useCreateUserWithEmailAndPassword,
  useSignInWithEmailAndPassword,
} from "react-firebase-hooks/auth";
import { signOut } from "firebase/auth";
import { useRouter } from "next/navigation";

type AuthContextType = {
  email: string;
  setEmail: React.Dispatch<React.SetStateAction<string>>;
  password: string;
  setPassword: React.Dispatch<React.SetStateAction<string>>;
  handleLogin: (event: React.FormEvent<HTMLFormElement>) => Promise<void>;
  handleSignUp: (event: React.FormEvent<HTMLFormElement>) => Promise<void>;
  authenticationError: string | null;
};

const AuthContext = createContext<AuthContextType | null>(null);

function AuthProvider({ children }: { children: React.ReactNode }) {
  // const [loading] = useAuthState(auth);
  const navigate = useRouter();

  // importing firebase auth context from react-firease and calling the destructing the value for sign up and login. these hooks return an array with the first element being a function to call to trigger the auth action, and the rest are user, loading and error states.
  const [createUserWithEmailAndPassword] =
    useCreateUserWithEmailAndPassword(auth);
  const [signInWithEmailAndPassword] = useSignInWithEmailAndPassword(auth);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [authenticationError, setAuthenticationError] = useState<string | null>(
    null,
  );

  const handleSignUp = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      const response = await createUserWithEmailAndPassword(email, password);
      const user = response?.user;
      console.log(user);
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  };

  const handleLogin = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const response = await signInWithEmailAndPassword(email, password);
      // console.log(response);

      if (response?.user) {
        navigate.push("/form");
      } else {
        setAuthenticationError("Please enter a valid email and password");
        setTimeout(() => {
          setAuthenticationError(null);
        }, 2000);
        return;
      }
    } catch (error: unknown) {
      // console.error(error);
      const firebaseError = error as { code?: string };

      if (firebaseError.code === "auth/invalid-credential") {
        setAuthenticationError("Invalid email or password.");
      } else if (firebaseError.code === "auth/too-many-requests") {
        setAuthenticationError("Too many attempts. Try again later.");
      } else if (firebaseError.code === "auth/user-disabled") {
        setAuthenticationError("This account has been disabled.");
      } else {
        setAuthenticationError("An error occurred. Please try again.");
      }

      setTimeout(() => setAuthenticationError(null), 2500);
    }

    //  this is usually called  "router". i find "navigate " a better name convention
    // "INVALID_LOGIN_CREDENTIALS // no user case
  };

  const value = {
    email,
    setEmail,
    password,
    setPassword,
    handleLogin,
    handleSignUp,
    authenticationError,
  };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("context must be used witin the AuthProvider !");
  }
  return context;
};
export { useAuth, AuthProvider };
