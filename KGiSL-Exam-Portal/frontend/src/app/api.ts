import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

/**
 * Authenticates an admin user.
 * @param username Admin username
 * @param password Admin password
 * @returns Promise with auth token and role
 */
export const loginAdmin = async (username: string, password: string) => {
  return api.post('/api/login/', { username, password, role: 'admin' });
};

/**
 * Authenticates a student user.
 * @param username Student register number
 * @param password Student password
 * @returns Promise with auth token and role
 */
export const loginStudent = async (username: string, password: string) => {
  return api.post('/api/login/', { username, password, role: 'student' });
};

/**
 * Uploads an Excel file containing exam/student data.
 * @param file The Excel file to upload
 */
export const uploadDataset = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/api/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

/**
 * Retrieves the list of uploaded datasets.
 * @returns Promise with list of datasets
 */
export const getDatasets = async () => {
  return api.get('/api/datasets/');
}

/**
 * Toggles the active state of a dataset by ID.
 * @param id The dataset ID to toggle
 */
export const toggleDataset = async (id: number) => {
  return api.post(`/api/datasets/${id}/toggle/`);
}

/**
 * Deletes all student data.
 * @returns Promise with deletion confirmation
 */
export const deleteStudents = async () => {
  return api.delete('/api/delete-all/');
}

/**
 * Authenticates a faculty member.
 * @param register_no Faculty register number
 * @param password Faculty password
 */
export const loginFaculty = async (register_no: string, password: string) => {
  return api.post('/api/faculty/login/', { register_no, password });
};

/**
 * Retrieves the dashboard data for a logged-in faculty.
 * @param token Auth token
 */
export const getFacultyDashboard = async (token: string) => {
  return api.get('/api/faculty/dashboard/', {
    headers: { 'Authorization': `Token ${token}` }
  });
};

/**
 * Gets student list for a specific hall and session.
 * @param token Auth token
 * @param hall_no Hall number
 * @param session Session (FN/AN)
 */
export const getFacultyStudents = async (token: string, hall_no: string, session: string) => {
  return api.get(`/api/faculty/students/?hall_no=${hall_no}&session=${session}`, {
    headers: { 'Authorization': `Token ${token}` }
  });
};

/**
 * Retrieves past duties for the logged-in faculty.
 * @param token Auth token
 */
export const getFacultyHistory = async (token: string) => {
  return api.get('/api/faculty/history/', {
    headers: { 'Authorization': `Token ${token}` }
  });
};

/**
 * Updates availability status for a specific allocation.
 * @param token Auth token
 * @param allocation_id Allocation ID
 * @param reason Reason for unavailability
 */
export const updateFacultyAvailability = async (token: string, allocation_id: number, reason: string) => {
  return api.post('/api/faculty/availability/update/', { allocation_id, reason }, {
    headers: { 'Authorization': `Token ${token}` }
  });
};

/**
 * Triggers the faculty allocation algorithm.
 * @param dept_counts Request counts per department
 * @param date Exam date
 * @param session Exam session
 * @param designation Target designation
 */
export const allocateFaculty = async (dept_counts: any, date: string, session: string, designation: string) => {
  return api.post('/api/faculty/admin/allocate/', { dept_counts, date, session, designation });
};

/**
 * Confirms the allocation for a date/session.
 * Makes it visible to faculty members.
 * @param date Exam date
 * @param session Exam session
 */
export const confirmFacultyAllocation = async (date: string, session: string) => {
  return api.post('/api/faculty/admin/confirm/', { date, session });
};

/**
 * Checks allocation status (confirmed/active) for a session.
 * @param date Exam date
 * @param session Exam session
 */
export const getFacultyStatus = async (date: string, session: string) => {
  return api.get(`/api/faculty/admin/status/?date=${date}&session=${session}`);
};

/**
 * Toggles visibility of allocation to faculty.
 * @param date Exam date
 * @param session Exam session
 * @param is_faculty_active Target visibility state
 */
export const toggleFacultyActive = async (date: string, session: string, is_faculty_active: boolean) => {
  return api.post('/api/faculty/admin/status/', { date, session, is_faculty_active });
};

/**
 * Retrieves list of allocated faculty for admin view.
 * @param date Exam date
 * @param session Exam session
 */
export const getAllocatedFaculty = async (date: string, session: string) => {
  return api.get(`/api/faculty/admin/list/?date=${date}&session=${session}`);
};

/**
 * Submits a request to valid reason for alternation.
 * @param token Auth token
 * @param allocation_id ID of usage allocation
 * @param reason Reason for requesting alternation
 */
export const requestAlternation = async (token: string, allocation_id: number, reason: string) => {
  return api.post('/api/faculty/alternation/request/', { allocation_id, reason }, {
    headers: { 'Authorization': `Token ${token}` }
  });
};

/**
 * Lists all alternation requests filtered by status.
 * @param status Filter status (PENDING/APPROVED/REJECTED)
 */
export const getAdminAlternationRequests = async (status: string = 'PENDING') => {
  return api.get(`/api/faculty/admin/alternation/requests/?status=${status}`);
};

/**
 * Approves or rejects an alternation request.
 * @param request_id Request ID
 * @param action Action (APPROVED/REJECTED)
 */
export const approveAlternationRequest = async (request_id: number, action: string) => {
  return api.post('/api/faculty/admin/alternation/approve/', { request_id, action });
};

export const default_api = api;
export default api;
