// src/features/user/userSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import initialState from "./initialState.json";
import UserState from "./type";
import { addUrlAsync } from "./asyncAction";

const mainVideoSlice = createSlice({
  name: "mainVideo",
  initialState,
  reducers: {
    setVideo(state, action: PayloadAction<UserState>) {
      state.img_url = action.payload.img_url;
      state.position = action.payload.position;
      state.description = action.payload.description;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(addUrlAsync.fulfilled, (state, action) => {
        state.img_url = action.payload.img_url;
        state.position = action.payload.position;
        state.description = action.payload.description;
      })
      .addCase(addUrlAsync.rejected, (state) => {
        state.img_url = "";
        state.position = "";
        state.description = "";
      });
  },
});

// Экспортируем действия и редюсер
// export const { setName, setAge, resetUser } = mainVideoSlice.actions;
export default mainVideoSlice.reducer;
