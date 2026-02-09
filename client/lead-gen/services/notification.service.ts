// services/notification.service.ts

import { api } from "@/lib/api";
import { NotificationListResponse } from "@/types/notifications.types";


/* -----------------------------
   GET all
----------------------------- */
export const getNotifications = async (
  userId: number,
): Promise<NotificationListResponse> => {
  const { data } = await api.get<NotificationListResponse>(
    "/notifications",
    {
      params: { user_id: userId },
    },
  );

  return data;
};

/* -----------------------------
   GET unread
----------------------------- */
export const getUnreadNotifications = async (
  userId: number,
): Promise<NotificationListResponse> => {
  const { data } = await api.get<NotificationListResponse>(
    "/notifications/unread",
    {
      params: { user_id: userId },
    },
  );

  return data;
};

/* -----------------------------
   mark read
----------------------------- */
export const markNotificationRead = async (
  id: number,
): Promise<{ success: boolean }> => {
  const { data } = await api.post(`/notifications/mark-read/${id}`);
  return data;
};

/* -----------------------------
   mark all read
----------------------------- */
export const markAllNotificationsRead = async (
  userId: number,
): Promise<{ success: boolean }> => {
  const { data } = await api.post(
    `/notifications/mark-all-read`,
    null,
    {
      params: { user_id: userId },
    },
  );

  return data;
};
