import { LoginProps } from "pages/Login/types";
import { get, post } from "./axios";
import { toast } from "react-toastify";
import { User } from "store/features/auth/types";

export class AuthService {

  async refreshLogin(refreshToken: string) {
    return post("users/login/refresh/", {refresh: refreshToken})
  }

  async login(data: LoginProps) {
    const response = await post("users/login/", data).catch((error) => toast.error(error));
    localStorage.setItem("access_token", response.access);
    localStorage.setItem("refresh_token", response.refresh);
    return response
  }

  async retrieveLogged(): Promise<any> {
    return get("users/retrieve-self/")
  }
}
