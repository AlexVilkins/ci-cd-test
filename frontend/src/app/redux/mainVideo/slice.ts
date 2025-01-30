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
    setPosition(state, action: PayloadAction<UserState>) {
      state.position = action.payload.position;
    },
    dropeState() {
      return initialState;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(addUrlAsync.fulfilled, (state, action) => {
        state.img_url = action.payload.img_url;
        state.position = action.payload.position;
        state.description = action.payload.description;
        state.panelType = "img";
      })
      .addCase(addUrlAsync.rejected, (state) => {
        state.img_url = "";
        state.position = 0;
        state.description = "";
      });
  },
});

export const { setPanelType, setButtonDesable, dropeState, setPosition } =
  mainVideoSlice.actions;
export default mainVideoSlice.reducer;
