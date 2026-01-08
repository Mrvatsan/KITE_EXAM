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

export const loginFaculty = async (register_no: string, password: string) => {
  return api.post('/api/faculty/login/', { register_no, password });
};

export const getFacultyDashboard = async (token: string) => {
  return api.get('/api/faculty/dashboard/', {
    headers: { 'Authorization': `Token ${token}` }
  });
};

export const getFacultyStudents = async (token: string, hall_no: string, session: string) => {
  return api.get(`/api/faculty/students/?hall_no=${hall_no}&session=${session}`, {
    headers: { 'Authorization': `Token ${token}` }
  });
};

export const getFacultyHistory = async (token: string) => {
  return api.get('/api/faculty/history/', {
    headers: { 'Authorization': `Token ${token}` }
  });
};

export const updateFacultyAvailability = async (token: string, allocation_id: number, reason: string) => {
  return api.post('/api/faculty/availability/update/', { allocation_id, reason }, {
    headers: { 'Authorization': `Token ${token}` }
  });
};

export const allocateFaculty = async (dept_counts: any, date: string, session: string, designation: string) => {
  return api.post('/api/faculty/admin/allocate/', { dept_counts, date, session, designation });
};

export const confirmFacultyAllocation = async (date: string, session: string) => {
  return api.post('/api/faculty/admin/confirm/', { date, session });
};

export const getFacultyStatus = async (date: string, session: string) => {
  return api.get(`/api/faculty/admin/status/?date=${date}&session=${session}`);
};

export const toggleFacultyActive = async (date: string, session: string, is_faculty_active: boolean) => {
  return api.post('/api/faculty/admin/status/', { date, session, is_faculty_active });
};

export const getAllocatedFaculty = async (date: string, session: string) => {
  return api.get(`/api/faculty/admin/list/?date=${date}&session=${session}`);
};

export const default_api = api;
export default api;
