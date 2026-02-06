import Logo from "@/components/logo"

export default function LoginSidePanel() {
  return (
    <div className="bg-muted h-screen p-5 max-lg:hidden">
      <div
        data-slot="card"
        className="text-card-foreground relative flex h-full flex-col justify-between gap-6 overflow-hidden rounded-xl border-none bg-primary py-8 shadow-sm"
      >
        <div
          data-slot="card-header"
          className="grid auto-rows-min grid-rows-[auto_auto] items-start gap-6 px-8"
        >
          <div
            data-slot="card-title"
            className="text-primary-foreground text-4xl font-bold xl:text-5xl/15.5"
          >
            Welcome back! Please sign in to your Lead Gen account
          </div>

          <p className="text-primary-foreground text-xl">
            Thank you for registering! Please check your inbox and click the
            verification link to activate your account.
          </p>
        </div>

        <Logo className="text-secondary/10 pointer-events-none absolute -left-50 bottom-30 size-130" />

        <div
          data-slot="card-content"
          className="relative z-1 mx-8 h-62 overflow-hidden rounded-2xl px-0"
        >
          <svg
            width="1094"
            height="249"
            viewBox="0 0 1094 249"
            fill="none"
            className="pointer-events-none absolute right-0 -z-1 select-none"
          >
            <path
              d="M0.263672 16.8809C0.263672 8.0443 7.42712 0.880859 16.2637 0.880859H786.394H999.115C1012.37 0.880859 1023.12 11.626 1023.12 24.8808L1023.12 47.3809C1023.12 60.6357 1033.86 71.3809 1047.12 71.3809H1069.6C1082.85 71.3809 1093.6 82.126 1093.6 95.3809L1093.6 232.881C1093.6 241.717 1086.43 248.881 1077.6 248.881H16.2637C7.42716 248.881 0.263672 241.717 0.263672 232.881V16.8809Z"
              fill="var(--card)"
            />
          </svg>

          <div className="bg-card absolute top-0 right-0 flex size-15 items-center justify-center rounded-2xl">
            <Logo className="size-15" />
          </div>

          <div className="flex flex-col gap-5 p-6">
            <p className="line-clamp-2 pr-12 text-3xl font-bold">
              Please enter your login details
            </p>

            <p className="line-clamp-2 text-lg">
              Stay connected with Lead Gen. Subscribe now for the latest updates
              and news.
            </p>

            <div className="flex -space-x-4 self-end">
              <span className="relative flex size-12 shrink-0 overflow-hidden rounded-full ring-2 ring-background">
                <img
                  className="aspect-square size-full"
                  src="https://cdn.shadcnstudio.com/ss-assets/avatar/avatar-3.png"
                />
              </span>

              <span className="relative flex size-12 shrink-0 overflow-hidden rounded-full ring-2 ring-background">
                <img
                  className="aspect-square size-full"
                  src="https://cdn.shadcnstudio.com/ss-assets/avatar/avatar-6.png"
                />
              </span>

              <span className="relative flex size-12 shrink-0 overflow-hidden rounded-full ring-2 ring-background">
                <img
                  className="aspect-square size-full"
                  src="https://cdn.shadcnstudio.com/ss-assets/avatar/avatar-5.png"
                />
              </span>

              <span className="relative flex size-12 shrink-0 items-center justify-center rounded-full bg-muted text-xs ring-2 ring-background">
                +3695
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
