// types/auth.types.ts

export interface LoginPayload {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: "bearer";
  id:number,
  name: string;
  email: string;
}
