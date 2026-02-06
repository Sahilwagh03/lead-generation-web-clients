import * as React from "react";
import { cn } from "@/lib/utils"; // optional (shadcn helper). If not using, remove.

type LogoProps = React.SVGProps<SVGSVGElement> & {
  size?: number | string;
};

const Logo: React.FC<LogoProps> = ({
  className,
  size = 60,
  ...props
}) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 128 128"
      width={size}
      height={size}
      fill="none"
      className={cn("inline-block", className)}
      {...props}
    >
      <path
        stroke="currentColor"
        strokeWidth={8.117}
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M63.673 24.849v24.54c0 8.07-6.54 14.611-14.61 14.611H25.204M64.327 103.152V78.611c0-8.07 6.54-14.61 14.61-14.61h23.859M93.347 35.611 76.555 52.205M51.77 77.062 34.978 93.657M50.958 51.319 34.265 34.626M93.162 93.64 76.469 76.946"
      />
    </svg>
  );
};

export default Logo;
