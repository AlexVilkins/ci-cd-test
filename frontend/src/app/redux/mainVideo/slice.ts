// src/features/user/userSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import initialState from "./initialState.json";
import UserState from "./type";
import { addUrlAsync } from "./asyncAction";

const mainVideoSlice = createSlice({
  name: "mainVideo",
  initialState,
  reducers: {
    setPanelType(state, action: PayloadAction<UserState>) {
      state.panelType = action.payload.panelType;
      state.img_url = action.payload.img_url;
    },
    setButtonDesable(state, action: PayloadAction<UserState>) {
      state.desableButton = action.payload.desableButton;
    },
    setDesableButton(state, action: PayloadAction<UserState>) {
      state.desableButton = action.payload.desableButton;
    }, // Контроль конопки
  },
  extraReducers: (builder) => {
    builder
      .addCase(addUrlAsync.fulfilled, (state, action) => {
        state.img_url = action.payload.img_url;
        state.position = action.payload.position;
        state.description = action.payload.description;
        state.panelType = "img";
        // state.desableButton = true;
      })
      .addCase(addUrlAsync.rejected, (state) => {
        state.img_url = "";
        state.position = 0;
        state.description = "";
      });
  },
});

// Экспортируем действия и редюсер
export const { setPanelType, setButtonDesable, setDesableButton } =
  mainVideoSlice.actions;
export default mainVideoSlice.reducer;
