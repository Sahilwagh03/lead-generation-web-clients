"use client";

type CookieOptions = {
  days?: number;
  seconds?: number;
  path?: string;
  secure?: boolean;
  sameSite?: "Lax" | "Strict" | "None";
};

export const useCookies = () => {
  /* ---------------------------------
     Set Cookie
  --------------------------------- */
  const setCookie = (
    name: string,
    value: string,
    options: CookieOptions = {}
  ) => {
    if (typeof document === "undefined") return;

    const {
      days = 1,
      seconds,
      path = "/",
      secure = false,
      sameSite = "Lax",
    } = options;

    let expires = "";

    if (seconds) {
      expires = `; max-age=${seconds}`;
    } else {
      const date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = `; expires=${date.toUTCString()}`;
    }

    document.cookie = [
      `${name}=${encodeURIComponent(value)}`,
      expires,
      `path=${path}`,
      `SameSite=${sameSite}`,
      secure ? "Secure" : "",
    ].join("; ");
  };

  /* ---------------------------------
     Get Cookie
  --------------------------------- */
  const getCookie = (name: string): string | null => {
    if (typeof document === "undefined") return null;

    const match = document.cookie.match(
      new RegExp(`(?:^|; )${name}=([^;]*)`)
    );

    return match ? decodeURIComponent(match[1]) : null;
  };

  /* ---------------------------------
     Remove Cookie
  --------------------------------- */
  const removeCookie = (name: string, path = "/") => {
    if (typeof document === "undefined") return;

    document.cookie = `${name}=; Max-Age=0; path=${path}`;
  };

  /* ---------------------------------
     Helpers
  --------------------------------- */
  const hasCookie = (name: string) => !!getCookie(name);

  return {
    setCookie,
    getCookie,
    removeCookie,
    hasCookie,
  };
};
