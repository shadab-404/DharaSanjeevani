const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

export async function apiRequest(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "API request failed");
  }

  return response.json();
}

export const getLatestSensor = () =>
  apiRequest("/sensors/latest");

export const getSensorHistory = () =>
  apiRequest("/sensors/history");

export const getCrops = () =>
  apiRequest("/crops/");

export const getAlerts = () =>
  apiRequest("/alerts/");

export const getIrrigationHistory = () =>
  apiRequest("/irrigation/history");