"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Bell, CheckCheck, Info, UserPlus, Target } from "lucide-react";
import { cn } from "@/lib/utils";
import { SectionHeader } from "@/components/dashboard/section-header";

import { useState } from "react";
import { useNotifications } from "@/hooks/useNotifications";
import { getNotificationIcons } from "@/lib/common";
import { formatDateTime } from "@/lib/batch-status";

export default function NotificationsPage() {
  const [tab, setTab] = useState("all");

  /* ✅ real backend hook */
  const {
    notifications,
    unreadCount,
    markRead,
    markAllRead,
    loading,
  } = useNotifications();

  /* -------------------------
     Filtering
  ------------------------- */
  const filtered = notifications.filter((n) => {
    if (tab === "unread") return !n.is_read;
    if (tab === "system") return n.type === "system";
    return true;
  });


  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <SectionHeader title="Notifications" />

          {unreadCount > 0 && (
            <Badge variant="destructive">{unreadCount} new</Badge>
          )}
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={() => markAllRead()}
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

      {/* List */}
      <Card className="rounded-2xl">
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
        </CardHeader>

        <CardContent className="p-0">
          <ScrollArea className="h-125">
            {loading ? (
              <div className="py-10 text-center text-muted-foreground">
                Loading...
              </div>
            ) : filtered.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
                <Bell className="mb-3 h-10 w-10 opacity-40" />
                No notifications
              </div>
            ) : (
              <div className="divide-y">
                {filtered.map((n) => (
                  <div
                    key={n.id}
                    onClick={() => markRead(n.id)}
                    className={cn(
                      "flex items-start gap-4 p-4 transition hover:bg-muted/40 cursor-pointer",
                      !n.is_read && "bg-muted/20",
                    )}
                  >
                    {/* Icon */}
                    <div className="mt-1 rounded-lg bg-muted p-2">
                      {getNotificationIcons(n.type)}
                    </div>

                    {/* Content */}
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium">{n.title}</p>

                        <span className="text-xs text-muted-foreground">
                          {formatDateTime(n.created_at)}
                        </span>
                      </div>

                      <p className="text-sm text-muted-foreground">
                        {n.message}
                      </p>
                    </div>

                    {!n.is_read && (
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
