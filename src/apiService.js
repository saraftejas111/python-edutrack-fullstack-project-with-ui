import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const asList = (request) => request.then((response) => ({
  ...response,
  data: Array.isArray(response.data) ? response.data : (response.data?.results ?? []),
}));

// User APIs
export const userAPI = {
  registerUser: (userData) => api.post('/user/register-user/', userData),
  loginUser: (loginData) => api.post('/user/login-user/', loginData),
  getAllUsers: () => asList(api.get('/user/get-all-user/')),
  getUserByUsername: (username) => api.get(`/user/get-user-by-username/${encodeURIComponent(username)}/`),
  updateUser: (userData) => api.put('/user/update-user/', userData),
  deleteUserByUsername: (username) => api.delete('/user/delete-user-by-username', { params: { username } }),
  getAllFaculty: () => asList(api.get('/user/get-all-faculty/')),
};

// Student APIs
export const studentAPI = {
  addStudent: (studentData) => api.post('/student/add-student/', studentData),
  getAllStudents: () => asList(api.get('/student/get-all-students/')),
  updateStudent: (studentData) => api.put('/student/update-student/', studentData),
  deleteStudent: (id) => api.delete(`/student/delete-student/${id}/`),
};

// Subject APIs
export const subjectAPI = {
  addSubject: (subjectData) => api.post('/subject/add-subject/', subjectData),
  getAllSubjects: () => asList(api.get('/subject/get-all-subjects/')),
  updateSubject: (subjectData) => api.put('/subject/update-subject/', subjectData),
  deleteSubject: (id) => api.delete(`/subject/delete-subject/${id}/`),
};

// Attendance APIs - FIXED THIS SECTION
export const attendanceAPI = {
  takeAttendance: (attendanceData) => api.post('/attendance/take-attendance/', attendanceData),
  getAllAttendanceRecords: () => asList(api.get('/attendance/get-all-attendance-records/')),
  getAttendance: (facultyUsername, subjectId, date) => 
    asList(api.get(`/attendance/get-attendance/${encodeURIComponent(facultyUsername)}/${subjectId}/${date}`)),
  getFilteredAttendance: (facultyUsername, subjectId, date) => {
    let url = '/attendance/get-attendance/';
    if (facultyUsername && subjectId && date) {
      url = `/attendance/get-attendance/${facultyUsername}/${subjectId}/${date}`;
    }
    return asList(api.get(url));
  },
};

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('username');
      localStorage.removeItem('role');
    }
    return Promise.reject(error);
  }
);

export default api;
