import axios from "axios";
import { useCookies } from "@/hooks/useCookies"; 

const { getCookie } = useCookies();
const getBaseURL = () => {
  // If env is provided → use it (production)
  if (process.env.NEXT_PUBLIC_API_BASE_URL) {
    return process.env.NEXT_PUBLIC_API_BASE_URL;
  }

  // Browser (mobile / LAN / desktop)
  if (typeof window !== "undefined") {
    const { protocol, hostname } = window.location;
    return `${protocol}//${hostname}:8000`;
  }

  // SSR fallback
  return "http://localhost:8000";
};

export const api = axios.create({
  baseURL: getBaseURL(),
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token = getCookie("token"); // 👈 from your cookie hook

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);
