import { User } from "models/User";

export interface AuthState {
  user?: User;
  accessToken?: string;
  refreshToken?: string;
  isRefreshing: boolean;
}
