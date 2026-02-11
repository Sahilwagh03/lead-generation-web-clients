"use client";

import { useState } from "react";
import { Bell, CheckCheck } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";

import { SectionHeader } from "@/components/dashboard/section-header";
import { EmptyState } from "@/components/empty-state";

import { useNotifications } from "@/hooks/useNotifications";
import { getNotificationIcons } from "@/lib/common";
import { formatDateTime } from "@/lib/batch-status";
import { cn } from "@/lib/utils";
import { NotificationsSkeleton } from "@/components/loading/notifications/notifications-skeleton";

import { NotificationDetailsDialog } from "@/components/dashboard/notifications/notification-details-dialog"

export default function NotificationsPage() {
  const [tab, setTab] = useState("all");

  const {
    notifications,
    unreadCount,
    markRead,
    markAllRead,
    loading,
  } = useNotifications();

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
          onClick={()=>markAllRead()}
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
        {
          !loading && filtered.length &&
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
        }

        <CardContent className="p-0">
          <ScrollArea className="h-100">
            {loading && <NotificationsSkeleton />}

            {!loading && filtered.length === 0 && (
              <div className="h-full flex items-center justify-center">
                <EmptyState
                  title="No notifications"
                  description="You're all caught up 🎉"
                  icon={<Bell className="h-8 w-8 text-muted-foreground" />}
                  cardClassName="border-0 shadow-none"
                />
              </div>
            )}

            {!loading && filtered.length > 0 && (
              <div className="divide-y">
                {filtered.map((n) => (
                  <NotificationDetailsDialog
                    key={n.id}
                    notification={n}
                  >
                    {/* Trigger row */}
                    <div
                      onClick={() => markRead(n.id)}
                      className={cn(
                        "flex items-start gap-4 p-4 cursor-pointer transition hover:bg-muted/40",
                        !n.is_read && "bg-muted/20"
                      )}
                    >
                      <div className="mt-1 rounded-lg bg-muted p-2">
                        {getNotificationIcons(n.type)}
                      </div>

                      <div className="flex-1 space-y-1">
                        <div className="flex items-center justify-between">
                          <p className="text-sm font-medium">{n.title}</p>

                          <span className="text-xs text-muted-foreground">
                            {formatDateTime(n.created_at)}
                          </span>
                        </div>

                        <p className="text-sm text-muted-foreground line-clamp-2">
                          {n.message}
                        </p>
                      </div>

                      {!n.is_read && (
                        <span className="mt-2 h-2 w-2 rounded-full bg-primary" />
                      )}
                    </div>
                  </NotificationDetailsDialog>
                ))}
              </div>
            )}
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}
