import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";

import { AuthState } from "./types"

const initialState = {
  user: undefined
} as AuthState;

export const authSlice = createSlice({
	name: "auth",
	initialState,
	reducers: {
		setLoggedIn: (state, action: PayloadAction<AuthState>) => {
			state.user = action.payload.user;
		},
		setLogout: () => initialState
	}
});

export const { setLoggedIn, setLogout } = authSlice.actions;
export default authSlice.reducer;
