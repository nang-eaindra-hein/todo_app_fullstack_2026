
import axios from 'axios';

export const axiosInstance = axios.create({
    baseURL: 'http://localhost:8001',
    headers: {
        'Content-Type': 'application/json',
    },
});

axiosInstance.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');

    console.log('TOKEN:', token);
    console.log('HEADERS:', config.headers);

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    console.log('AUTH:', config.headers.Authorization);

    return config;
});
axiosInstance.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/';  
    }
    return Promise.reject(error);
  }
);