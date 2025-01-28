// src/app/store.ts
import { useDispatch, useSelector, TypedUseSelectorHook } from "react-redux";

import { configureStore } from "@reduxjs/toolkit";
import mainVideoSlice from "./mainVideo/slice";

const store = configureStore({
  reducer: {
    mainVideoSlice,
  },
});

export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
export const useAppDispatch = () => useDispatch<AppDispatch>();

export default store;
