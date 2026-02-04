export type BatchStatus =
  | "PENDING"
  | "RUNNING"
  | "PROCESSED"
  | "COMPLETED"
  | "FAILED";


export const getBatchStatusStyles = (status: BatchStatus) => {
  const styles: Record<BatchStatus, string> = {
    COMPLETED:
      "bg-green-100 text-green-700 border-green-200",

    RUNNING:
      "bg-blue-100 text-blue-700 border-blue-200",

    PENDING:
      "bg-yellow-100 text-yellow-700 border-yellow-200",

    PROCESSED:
      "bg-purple-100 text-purple-700 border-purple-200",

    FAILED:
      "bg-red-100 text-red-700 border-red-200",
  };

  return styles[status] ?? "bg-gray-100 text-gray-600 border-gray-200";
};


export const capitalizeWords = (value: string): string => {
  return value
    .toLowerCase()
    .split("_")
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
};


export const formatDateTime = (value: string | Date): string => {
  const date = typeof value === "string" ? new Date(value) : value;

  return new Intl.DateTimeFormat("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
};
