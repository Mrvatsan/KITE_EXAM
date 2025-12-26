import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

export const loginAdmin = async (username: string, password: string) => {
  return api.post('/api/login/', { username, password, role: 'admin' });
};

export const loginStudent = async (username: string, password: string) => {
  return api.post('/api/login/', { username, password, role: 'student' });
};

export const uploadDataset = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/api/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getDatasets = async () => {
  return api.get('/api/datasets/');
}

export const toggleDataset = async (id: number) => {
  return api.post(`/api/datasets/${id}/toggle/`);
}

export const deleteStudents = async () => {
  return api.delete('/api/delete-all/');
}

export default api;
