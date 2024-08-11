import axios from 'axios';

//const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
//const API_URL = process.env.REACT_APP_API_URL || 'https://onemillionhaas-b249dc0f125a.herokuapp.com/';
const API_URL = 'https://onemillionhaas-b249dc0f125a.herokuapp.com/api';


const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = (username, password) => api.post('/login', { username, password });
export const register = (username, password) => api.post('/register', { username, password });
export const getProjects = () => api.get('/projects');
export const createProject = (project) => api.post('/projects', project);
export const getResources = () => api.get('/resources');
export const createResource = (name, capacity) => api.post('/resources', { name, capacity });
export const checkoutResources = (name, quantity, project_id) => api.post('/resources/checkout', { name, quantity, project_id });
export const checkinResources = (name, quantity, project_id) => api.post('/resources/checkin', { name, quantity, project_id });
export const getProjectResources = (project_id) => api.get(`/projects/${project_id}/resources`);

export default api;