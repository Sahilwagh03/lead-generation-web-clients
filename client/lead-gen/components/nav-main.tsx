"use client";

import { ChevronRight, type LucideIcon } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";

import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar";

import { cn } from "@/lib/utils";

export function NavMain({
  items,
  Navtitle,
}: {
  items: {
    title: string;
    url: string;
    icon?: LucideIcon;
    subitems?: {
      title: string;
      url: string;
      icon?: LucideIcon;
    }[];
  }[];
  Navtitle?: string;
}) {
  const pathname = usePathname();

  const isExactActive = (url: string) => pathname === url;
  const isSubActive = (url: string) => pathname.startsWith(url + "/");

  return (
    <SidebarGroup>
      {Navtitle && <SidebarGroupLabel>{Navtitle}</SidebarGroupLabel>}

      <SidebarMenu>
        {items.map((item) => {
          const active = isExactActive(item.url);

          if (!item.subitems?.length) {
            return (
              <SidebarMenuItem key={item.title}>
                <SidebarMenuButton
                  asChild
                  tooltip={item.title}
                  className={cn(active && "bg-primary/10 text-primary font-medium")}
                >
                  <Link href={item.url}>
                    {item.icon && <item.icon className="mr-2 w-5 h-5" />}
                    <span>{item.title}</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            );
          }

          const isOpen = item.subitems.some((s) => isSubActive(s.url));

          return (
            <Collapsible
              key={item.title}
              asChild
              defaultOpen={isOpen}
              className="group/collapsible"
            >
              <SidebarMenuItem>
                <CollapsibleTrigger asChild>
                  <SidebarMenuButton>
                    {item.icon && <item.icon className="mr-2 w-5 h-5" />}
                    <span>{item.title}</span>
                    <ChevronRight className="ml-auto w-4 h-4 transition-transform group-data-[state=open]/collapsible:rotate-90" />
                  </SidebarMenuButton>
                </CollapsibleTrigger>

                <CollapsibleContent>
                  <SidebarMenuSub>
                    {item.subitems.map((subItem) => {
                      const subActive = isExactActive(subItem.url);

                      return (
                        <SidebarMenuSubItem key={subItem.title}>
                          <SidebarMenuSubButton
                            asChild
                            className={cn(
                              subActive && "bg-primary/10 text-primary font-medium"
                            )}
                          >
                            <Link href={subItem.url}>
                              {subItem.icon && (
                                <subItem.icon className="mr-2 w-4 h-4" />
                              )}
                              <span>{subItem.title}</span>
                            </Link>
                          </SidebarMenuSubButton>
                        </SidebarMenuSubItem>
                      );
                    })}
                  </SidebarMenuSub>
                </CollapsibleContent>
              </SidebarMenuItem>
            </Collapsible>
          );
        })}
      </SidebarMenu>
    </SidebarGroup>
  );
}
