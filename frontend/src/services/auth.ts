import { LoginProps } from "pages/Login/types";
import { get, post } from "./axios";
import { toast } from "react-toastify";
import { User } from "store/features/auth/types";

export class AuthService {

  async refreshLogin(refreshToken: string) {
    return post("users/login/refresh/", {refresh: refreshToken})
  }

  async login(data: LoginProps) {
    return post("users/login/", data).catch((error) => toast.error(error))
  }

  async retrieveLogged(): Promise<User> {
    return get("users/retrieve-self")
  }
}
