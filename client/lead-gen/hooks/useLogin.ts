import { useMutation } from "@tanstack/react-query";
import { loginUser } from "@/services/auth.service";
import { LoginPayload, LoginResponse } from "@/types/auth.types";
import { useCookies } from "@/hooks/useCookies";
import { useAuth } from "@/context/auth-context";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

export const useLogin = () => {
  const { setCookie } = useCookies();
  const { setUser } = useAuth();
  const router = useRouter();

  return useMutation<LoginResponse, Error, LoginPayload>({
    mutationFn: loginUser,

    onSuccess: (data) => {
      setCookie("token", data.access_token);
      setCookie("user", JSON.stringify(data));

      setUser(data);

      toast.success("Logged in successfully")
      router.push("/dashboard");
    },

    onError: (error) => {
      toast.error("Invalid email or password")
    },
  });
};
