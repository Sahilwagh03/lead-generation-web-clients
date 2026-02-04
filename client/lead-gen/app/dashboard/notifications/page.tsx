"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Bell, CheckCheck, Info, UserPlus, Target } from "lucide-react";
import { cn } from "@/lib/utils";
import { SectionHeader } from "@/components/dashboard/section-header";

type Notification = {
  id: string;
  title: string;
  description: string;
  time: string;
  read: boolean;
  type: "lead" | "system" | "user";
};

const mockNotifications: Notification[] = [
  {
    id: "1",
    title: "New Lead Captured",
    description: "5 new leads added to Batch #21",
    time: "2 min ago",
    read: false,
    type: "lead",
  },
  {
    id: "2",
    title: "Batch Completed",
    description: "Scraping batch #18 finished successfully",
    time: "1 hour ago",
    read: false,
    type: "system",
  },
  {
    id: "3",
    title: "New Team Member",
    description: "Rahul joined your workspace",
    time: "Yesterday",
    read: true,
    type: "user",
  },
];

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState(mockNotifications);
  const [tab, setTab] = useState("all");

  const unreadCount = notifications.filter((n) => !n.read).length;

  const markAllRead = () =>
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));

  const filtered = notifications.filter((n) => {
    if (tab === "unread") return !n.read;
    if (tab === "system") return n.type === "system";
    return true;
  });

  const getIcon = (type: string) => {
    switch (type) {
      case "lead":
        return <Target className="h-4 w-4" />;
      case "user":
        return <UserPlus className="h-4 w-4" />;
      default:
        return <Info className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <SectionHeader
            title="Notifications"
          />

          {unreadCount > 0 && (
            <Badge variant="destructive">{unreadCount} new</Badge>
          )}
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={markAllRead}
          className="gap-2"
        >
          <CheckCheck className="h-4 w-4" />
          Mark all read
        </Button>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="all" onValueChange={setTab}>
        <TabsList>
          <TabsTrigger value="all">All</TabsTrigger>
          <TabsTrigger value="unread">Unread</TabsTrigger>
          <TabsTrigger value="system">System</TabsTrigger>
        </TabsList>
      </Tabs>

      {/* Notifications List */}
      <Card className="rounded-2xl">
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>

        <CardContent className="p-0">
          <ScrollArea className="h-125">
            {filtered.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
                <Bell className="mb-3 h-10 w-10 opacity-40" />
                No notifications
              </div>
            ) : (
              <div className="divide-y">
                {filtered.map((n) => (
                  <div
                    key={n.id}
                    className={cn(
                      "flex items-start gap-4 p-4 transition hover:bg-muted/40 cursor-pointer",
                      !n.read && "bg-muted/20",
                    )}
                  >
                    {/* Icon */}
                    <div className="mt-1 rounded-lg bg-muted p-2">
                      {getIcon(n.type)}
                    </div>

                    {/* Content */}
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium">{n.title}</p>

                        <span className="text-xs text-muted-foreground">
                          {n.time}
                        </span>
                      </div>

                      <p className="text-sm text-muted-foreground">
                        {n.description}
                      </p>
                    </div>

                    {/* unread dot */}
                    {!n.read && (
                      <span className="mt-2 h-2 w-2 rounded-full bg-primary" />
                    )}
                  </div>
                ))}
              </div>
            )}
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}
