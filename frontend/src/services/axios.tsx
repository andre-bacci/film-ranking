import axios, { AxiosResponse } from "axios";
import { AuthService } from "./auth";
import { Store } from "redux";
import { RootState } from "store";
import { setAccessToken, setIsRefreshing } from "store/features/auth/authSlice";

let api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

let store: Store<RootState>;

export const injectStore = (_store: Store<RootState>) => {
  store = _store;
};

api.interceptors.request.use((config) => {
  const access = store.getState().auth.accessToken;
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

// test needed
api.interceptors.response.use(
  (response) => {
    return response;
  },
  function (error) {
    const authService = new AuthService();
    const originalRequest = error.config;

    if (
      error.response.status === 401 &&
      originalRequest.url ===
        `${process.env.REACT_APP_API_URL}/api/users/login/`
    ) {
      return Promise.reject(error);
    }

    if (error.response.status === 401 && !store.getState().auth.isRefreshing) {
      store.dispatch(setIsRefreshing(true));
      const refreshToken = store.getState().auth.refreshToken;
      if (refreshToken)
        return authService.refreshLogin(refreshToken).then((res) => {
          if (res.status === 201) {
            store.dispatch(setIsRefreshing(false));
            store.dispatch(setAccessToken(res.data));
            return axios(originalRequest);
          }
        });
    }
    return Promise.reject(error);
  }
);

const get = async (url: string, config?: any) => {
  const response: AxiosResponse = await api.get(url, config);
  return response.data;
};

const patch = async (url: string, data: any) => {
  const response: AxiosResponse = await api.patch(url, data);
  return response.data;
};

const put = async (url: string, data: any, config?: any) => {
  const response: AxiosResponse = await api.put(url, data, config || {});
  return response.data;
};

const post = async (url: string, data: any, config?: any) => {
  const response: AxiosResponse = await api.post(url, data, config || {});
  return response.data;
};

const remove = async (url: string, config?: any) => {
  const response: AxiosResponse = await api.delete(url, config || {});
  return response.data;
};

export { get, patch, post, put, remove };
