
import { apiRequest } from "./api";

// Get all crops
export const getAllCrops = () =>
  apiRequest("/crops/");

// Add new crop
export const createCrop = (cropData) =>
  apiRequest("/crops/", {
    method: "POST",
    body: JSON.stringify(cropData),
  });

// Get crop by ID
export const getCropById = (cropId) =>
  apiRequest(`/crops/${cropId}`);

// Delete crop
export const deleteCrop = (cropId) =>
  apiRequest(`/crops/${cropId}`, {
    method: "DELETE",
  });
