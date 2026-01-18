"use client";

import { ChevronRight, type LucideIcon } from "lucide-react";
import Link from "next/link";

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

export function NavMain({
  items,Navtitle
}: {
  items: {
    title: string;
    url: string;
    icon?: LucideIcon
    isActive?: boolean;
    isOpen?: boolean;
    subitems?: {
      title: string;
      url: string;
      icon?: LucideIcon
    }[];
  }[],
  Navtitle?:string
}) {
  return (
    <SidebarGroup>
      {
        Navtitle && <SidebarGroupLabel>{Navtitle}</SidebarGroupLabel>
      }
      <SidebarMenu>
        {items.map((item) => {
          // If there are no subitems, render a simple menu item with a tooltip
          if (!item.subitems || item.subitems.length === 0) {
            return (
              <SidebarMenuItem key={item.title}>
                <SidebarMenuButton tooltip={item.title} asChild>
                  <Link href={item.url}>
                    {item.icon && <item.icon className="mr-2 w-6 h-6" />} {/* Increased icon size */}
                    <span>{item.title}</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            );
          }

          // If there are subitems, render the collapsible version with tooltip
          return (
            <Collapsible
              key={item.title}
              asChild
              defaultOpen={item.isOpen} // Using isOpen property from JSON
              className="group/collapsible"
            >
              <SidebarMenuItem>
                <CollapsibleTrigger asChild>
                  <SidebarMenuButton tooltip={item.title}>
                    {item.icon && <item.icon className="mr-2 w-6 h-6" />} {/* Increased icon size */}
                    <span>{item.title}</span>
                    <ChevronRight className="ml-auto w-5 h-5 transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
                  </SidebarMenuButton>
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <SidebarMenuSub>
                    {item.subitems.map((subItem) => (
                      <SidebarMenuSubItem key={subItem.title}>
                        <SidebarMenuSubButton asChild>
                          <Link href={subItem.url}>
                            {subItem.icon && <subItem.icon className="mr-2 w-5 h-5" />} {/* Increased icon size */}
                            <span>{subItem.title}</span>
                          </Link>
                        </SidebarMenuSubButton>
                      </SidebarMenuSubItem>
                    ))}
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