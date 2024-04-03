import { LoginProps } from "pages/Login/types";
import { get, post } from "./axios";
import { toast } from "react-toastify";
import { User } from "store/features/auth/types";
import Cookies from "js-cookie";

export class AuthService {

  async refreshLogin(refreshToken: string) {
    return post("users/login/refresh/", {refresh: refreshToken})
  }

  async login(data: LoginProps) {
    const response = await post("users/login/", data).catch((error) => toast.error(error))
    Cookies.set("access_token", response.access)
    Cookies.set("refresh_token", response.refresh)
  }

  async retrieveLogged(): Promise<User> {
    return get("users/retrieve-self/")
  }
}
