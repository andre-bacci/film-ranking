import axios, { AxiosResponse } from "axios";

let api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

api.interceptors.request.use((config) => {
  const access = localStorage.getItem("access_token");
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

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
