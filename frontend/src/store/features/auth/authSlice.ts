import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

import { AuthState } from "./types"
import { User } from "models/User";

const initialState = {
  user: undefined,
	accessToken: undefined,
	refreshToken: undefined,
	isRefreshing: false,
} as AuthState;

export const authSlice = createSlice({
	name: "auth",
	initialState,
	reducers: {
		setLoggedIn: (state, action: PayloadAction<User>) => {
			state.user = action.payload;
		},
		setLogout: () => initialState,
		setIsRefreshing: (state, action: PayloadAction<boolean>) => {
			state.isRefreshing = action.payload;
		},
		setAccessToken: (state, action: PayloadAction<string>) => {
			state.accessToken = action.payload;
		},
		setRefreshToken: (state, action: PayloadAction<string>) => {
			state.refreshToken = action.payload;
		},
	}
});

export const { setLoggedIn, setLogout, setIsRefreshing, setAccessToken, setRefreshToken } = authSlice.actions;
export default authSlice.reducer;
