import axiosCreate from "../axiosCreate";
import Order from "./type";

export const addUrl = async (url: string): Promise<Order> => {
  const response = await axiosCreate.post(`/youtube/add_url?url=${url}`);
  console.log("Backend response:", response.data);
  return response.data;
};
