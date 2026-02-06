import { GalleryVerticalEnd } from "lucide-react";

import { LoginForm } from "@/components/login-form";
import Logo from "@/components/logo";
import LoginSidePanel from "@/components/login-side-panel";

export default function LoginPage() {
  return (
    <div className="grid min-h-svh lg:grid-cols-2">
      <div className="flex justify-center items-center flex-col gap-4 p-6 md:p-10">
        <LoginForm />
      </div>
      <div className="bg-muted relative hidden lg:block">
        <LoginSidePanel />
      </div>
    </div>
  );
}
