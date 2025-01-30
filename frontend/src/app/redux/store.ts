// src/app/store.ts

import { configureStore } from "@reduxjs/toolkit";
import mainVideoSlice from "./mainVideo/slice";

export const store = configureStore({
  reducer: {
    mainVideoSlice,
  },
});

export type AppStore = typeof store;
export type RootState = ReturnType<AppStore["getState"]>;
export type AppDispatch = AppStore["dispatch"];
