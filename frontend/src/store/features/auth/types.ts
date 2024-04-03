export interface User {
  id: string;
  name: string;
  isActive: boolean;
  email: string;
}

export interface AuthState {
  user?: User;
}
