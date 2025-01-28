import { createAsyncThunk } from "@reduxjs/toolkit";
import { addUrl } from "@app/api/addUrl/addUrl";
import Order from "@app/api/addUrl/addUrl/type";

export const addUrlAsync = createAsyncThunk<Order>(
  "mainVideo/addUrl",
  async (url) => {
    const response = await addUrl(url);
    return response;
  }
);
