import axios from 'axios';

const client = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
});

client.interceptors.request.use(config => {
  const token = localStorage.getItem('nhatki_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

client.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401 && window.location.pathname !== '/login') {
      localStorage.removeItem('nhatki_token');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default client;
