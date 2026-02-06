import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",

  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },

  allowedDevOrigins: [
    "192.168.0.109",
    "local-origin.dev",
    "*.local-origin.dev",
  ],
};

export default nextConfig;
