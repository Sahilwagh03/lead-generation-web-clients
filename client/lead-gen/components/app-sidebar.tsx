"use client"

import * as React from "react"
import { NavMain } from "@/components/nav-main"
import { TeamSwitcher } from "@/components/team-switcher"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"
import { SidebarData } from "@/constant/dashboard"
import Logo from "./logo"
import { LogoutButton } from "./logout-button"

const data = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  teams: [
    {
      name: "LeadGen",
      logo: Logo,
      plan: "Enterprise",
    }
  ]
}



export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <TeamSwitcher teams={data.teams} />
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={SidebarData} />
      </SidebarContent>
      <SidebarRail />
      <SidebarFooter>
        <LogoutButton/>
      </SidebarFooter>
    </Sidebar>
  )
}