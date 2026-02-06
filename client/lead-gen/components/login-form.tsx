"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Field,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import { Eye, EyeOff } from "lucide-react";
import Logo from "@/components/logo";
import { useLogin } from "@/hooks/useLogin";

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"form">) {
  const [showPassword, setShowPassword] = useState(false);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [errors, setErrors] = useState<{
    email?: string;
    password?: string;
  }>({});

  const { mutate: login, isPending } = useLogin();

  // ✅ simple validation
  const validate = () => {
    const newErrors: typeof errors = {};

    if (!email) newErrors.email = "Email is required";
    else if (!/\S+@\S+\.\S+/.test(email)) newErrors.email = "Invalid email";

    if (!password) newErrors.password = "Password is required";
    else if (password.length < 6) newErrors.password = "Minimum 6 characters";

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    login({
      email,
      password,
    });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={cn("flex w-full flex-col gap-6 p-6 sm:max-w-lg", className)}
      {...props}
    >
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="flex size-9 items-center justify-center rounded-full bg-black dark:bg-white">
          <Logo className="size-8 text-white dark:text-black" />
        </div>
        <span className="text-xl font-semibold">Lead Gen</span>
      </div>

      {/* Title */}
      <div>
        <h2 className="mb-1.5 text-2xl font-semibold">Welcome Back</h2>
        <p className="text-muted-foreground">
          Sign in to your account to continue
        </p>
      </div>

      <FieldGroup className="space-y-2">
        <Field>
          <FieldLabel htmlFor="userEmail">Email</FieldLabel>

          <Input
            id="userEmail"
            type="email"
            placeholder="Enter your email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          {errors.email && <FieldError>{errors.email}</FieldError>}
        </Field>

        <Field>
          <FieldLabel htmlFor="password">Password</FieldLabel>

          <div className="relative">
            <Input
              id="password"
              type={showPassword ? "text" : "password"}
              placeholder="••••••••••••••••"
              className="pr-10"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <button
              type="button"
              onClick={() => setShowPassword((p) => !p)}
              className="text-muted-foreground absolute inset-y-0 right-0 flex size-9 items-center justify-center hover:text-foreground"
            >
              {showPassword ? (
                <EyeOff className="size-4" />
              ) : (
                <Eye className="size-4" />
              )}
            </button>
          </div>

          {errors.password && <FieldError>{errors.password}</FieldError>}
        </Field>

        {/* Remember + Forgot */}
        <div className="flex items-center justify-between text-sm">
          <label className="text-muted-foreground flex items-center gap-2">
            <input type="checkbox" className="size-4" />
            Remember Me
          </label>

          <a href="#" className="hover:underline">
            Forgot Password?
          </a>
        </div>

        <Button type="submit" className="w-full" disabled={isPending}>
          {isPending ? "Signing in..." : "Sign in"}
        </Button>
      </FieldGroup>
    </form>
  );
}
