import axios from 'axios';

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
export const getAllProjects = () => api.get('/all-projects');
export const createProject = (project) => api.post('/projects', project);
export const joinProject = (projectId) => api.post('/join-project', { project_id: projectId });
export const getResources = () => api.get('/resources');
export const checkoutResources = (hw_set, quantity, project_id) => api.post('/resources/checkout', { hw_set, quantity, project_id });
export const checkinResources = (hw_set, quantity, project_id) => api.post('/resources/checkin', { hw_set, quantity, project_id });
export const getProjectResources = (project_id) => api.get(`/projects/${project_id}/resources`);

export default api;