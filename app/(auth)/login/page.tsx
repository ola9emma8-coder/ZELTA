"use client";

import { useAuth } from "@/context/authContext";
import React, { JSX } from "react";
import LoginForm from "./LoginForm";
// import LoginForm from "@/app/auth/login/LoginForm";
// import { auth } from "@/firebase";

function Login(): JSX.Element {
  const {
    email,
    password,
    setEmail,
    setPassword,
    handleLogin,
    authenticationError,
  } = useAuth();
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-10 relative">
      {
        <LoginForm
          email={email}
          password={password}
          setEmail={setEmail}
          setPassword={setPassword}
          handleLogin={handleLogin}
          authenticationError={authenticationError}
        />
      }
    </div>
  );
}

export default Login;
