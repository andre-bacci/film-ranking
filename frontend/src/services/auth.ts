import { LoginProps } from "pages/Login/types";
import { get, post } from "./axios";
import { toast } from "react-toastify";
import { UserData } from "models/User";

export class AuthService {

  async refreshLogin(refreshToken: string) {
    return post("users/login/refresh/", {refresh: refreshToken})
  }

  async login(data: LoginProps) {
    const response = await post("users/login/", data).catch((error) => toast.error(error));
    return response
  }

  async retrieveLogged(): Promise<UserData> {
    return get("users/retrieve-self/")
  }
}
