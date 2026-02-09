"use client";

import { useEffect, useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";

import {
  getNotifications,
  markNotificationRead,
  markAllNotificationsRead,
} from "@/services/notification.service";

import { Notification } from "@/types/notifications.types";
import { useCookies } from "@/hooks/useCookies";

export const useNotifications = () => {
  const queryClient = useQueryClient();
  const { getCookie } = useCookies();

  /* -------------------------
     SSR SAFE userId
  ------------------------- */
  const [userId, setUserId] = useState<number | null>(null);

  useEffect(() => {
    const raw = getCookie("user");

    if (!raw) return;

    try {
      const parsed = JSON.parse(raw);
      setUserId(parsed?.id ?? null);
    } catch {
      setUserId(null);
    }
  }, [getCookie]);

  /* -------------------------
     Fetch notifications
  ------------------------- */
  const query = useQuery<Notification[]>({
    queryKey: ["notifications", userId],
    queryFn: () => getNotifications(userId!),
    enabled: !!userId, // only after cookie ready
  });

  /* -------------------------
     Mark single read
  ------------------------- */
  const markReadMutation = useMutation({
    mutationFn: markNotificationRead,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["notifications", userId],
      });
    },

    onError: () => {
      toast.error("Failed to mark as read");
    },
  });

  /* -------------------------
     Mark all read
  ------------------------- */
  const markAllMutation = useMutation({
    mutationFn: () => markAllNotificationsRead(userId!),

    onSuccess: () => {
      toast.success("All notifications marked as read");

      queryClient.invalidateQueries({
        queryKey: ["notifications", userId],
      });
    },
  });

  /* -------------------------
     Derived helpers
  ------------------------- */
  const notifications = query.data ?? [];

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  return {
    notifications,
    unreadCount,

    loading: query.isLoading || userId === null,

    markRead: markReadMutation.mutate,
    markReadAsync: markReadMutation.mutateAsync,
    markAllRead: markAllMutation.mutate,

    refetch: query.refetch,
  };
};
