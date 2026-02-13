"use client";

import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { formatDateTime } from "@/lib/batch-status";
import DynamicTabs from "./dynamic-tabs";
import { NotificationDataViewTabs } from "@/constant/dashboard";

type Props = {
  notification: {
    title: string;
    created_at: string;
    message: string;
  };
  children: React.ReactNode;
};

export function NotificationDetailsDialog({ notification, children }: Props) {
  return (
    <Dialog>
      <DialogTrigger asChild>{children}</DialogTrigger>

      <DialogContent className="p-4 max-w-[95vw]! max-h-[95vh] flex flex-col overflow-hidden">
        <DialogHeader>
          <DialogTitle className="text-lg font-semibold">
            {notification.title}
          </DialogTitle>

          <DialogDescription className="flex flex-col gap-1">
            <span>{formatDateTime(notification.created_at)}</span>
            <span>{notification.message}</span>
          </DialogDescription>
        </DialogHeader>
        <DynamicTabs tabs={NotificationDataViewTabs} />
      </DialogContent>
    </Dialog>
  );
}
