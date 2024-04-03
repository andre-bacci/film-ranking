import axios, { AxiosResponse } from "axios";

let api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
});

api.interceptors.request.use(
  (config: any) => {
    const newConfig = {
      ...config,
      headers: {
        ...config.headers,
      },
    };
    return newConfig;
  },
  (error: any) => Promise.reject(error)
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
