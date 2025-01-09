import axiosInstance from "./axiosCreate";

interface Data {
  id: string;
  name: string;
  age: number;
  city: string | null;
}

export const getData = async () => {
  const response = await axiosInstance.post<Data[]>("/user/all");
  console.log(response);
  return response.data;
};

export default getData;
