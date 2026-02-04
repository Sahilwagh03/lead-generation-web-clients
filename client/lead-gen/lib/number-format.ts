export const formatCount = (value: number | string): string => {
  const num = typeof value === "string" ? Number(value) : value;

  if (isNaN(num)) return String(value);

  if (num < 1000) return String(num);

  const units = ["K", "M", "B", "T"];
  let unitIndex = -1;
  let formatted = num;

  while (formatted >= 1000 && unitIndex < units.length - 1) {
    formatted /= 1000;
    unitIndex++;
  }

  return `${parseFloat(formatted.toFixed(1))}${units[unitIndex]}`;
};
