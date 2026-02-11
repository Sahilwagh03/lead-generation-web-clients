"use client";

import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

import { formatDateTime } from "@/lib/batch-status";

type Props = {
  notification: any;
  children: React.ReactNode;
};

export function NotificationDetailsDialog({
  notification,
  children,
}: Props) {
  return (
    <Dialog>
      {/* trigger passed as child */}
      <DialogTrigger asChild>{children}</DialogTrigger>

      <DialogContent className="sm:max-w-lg rounded-2xl p-6">
        <DialogHeader>
          <DialogTitle className="text-lg font-semibold">
            {notification.title}
          </DialogTitle>

          <DialogDescription>
            {formatDateTime(notification.created_at)}
          </DialogDescription>
        </DialogHeader>

        {/* message */}
        <p className="pt-3 text-sm text-muted-foreground">
          {notification.message}
        </p>

        {/* stats grid */}
        {notification.stats && (
          <div className="grid grid-cols-2 gap-3 pt-5">
            {Object.entries(notification.stats).map(([key, val]) => (
              <Button
                key={key}
                variant="secondary"
                className="justify-between h-11 capitalize font-medium"
              >
                {key}
                <Badge variant="outline">{val as number}</Badge>
              </Button>
            ))}
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
