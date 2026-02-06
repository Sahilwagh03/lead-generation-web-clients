export const useCookies = () => {
  const setCookie = (
    name: string,
    value: string,
    days = 1
  ) => {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);

    document.cookie = `${name}=${encodeURIComponent(
      value
    )}; expires=${expires.toUTCString()}; path=/`;
  };

  const getCookie = (name: string) => {
    const match = document.cookie.match(
      new RegExp("(^| )" + name + "=([^;]+)")
    );

    return match ? decodeURIComponent(match[2]) : null;
  };

  const removeCookie = (name: string) => {
    document.cookie = `${name}=; Max-Age=0; path=/`;
  };

  return { setCookie, getCookie, removeCookie };
};
