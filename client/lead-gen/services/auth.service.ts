import { api } from "@/lib/api";
import { LoginPayload, LoginResponse } from "@/types/auth.types";

export const loginUser = async (
  payload: LoginPayload
): Promise<LoginResponse> => {
  const res = await api.post("/login", payload);

  return res.data;
};