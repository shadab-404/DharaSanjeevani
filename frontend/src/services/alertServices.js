
import { apiRequest } from "./api";

// Resolve an alert
export const resolveAlert = (alertId) =>
  apiRequest(`/alerts/${alertId}/resolve`, {
    method: "PATCH",
  });
