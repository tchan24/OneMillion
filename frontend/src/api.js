import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  console.log('Making request to:', config.url);
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  console.error('Request error:', error);
  return Promise.reject(error);
});

api.interceptors.response.use((response) => {
  console.log('Received response:', response.status, response.data);
  return response;
}, (error) => {
  console.error('Response error:', error);
  if (error.response) {
    console.error('Response data:', error.response.data);
    console.error('Response status:', error.response.status);
  }
  return Promise.reject(error);
});

export const login = (username, password) => api.post('/login', { username, password });
export const register = (username, password) => api.post('/register', { username, password });
export const getProjects = () => api.get('/projects');
export const createProject = (projectData) => api.post('/projects', projectData);
export const getResources = () => api.get('/resources');
export const checkoutResources = (resourceData) => api.post('/resources/checkout', resourceData);
export const checkinResources = (resourceData) => api.post('/resources/checkin', resourceData);

export default api;