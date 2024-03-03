// import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css';
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import axios from 'axios'


axios.defaults.baseURL = 'http://127.0.0.1:8000/';

// Function to get the access token from localStorage
function getAccessToken() {
    return localStorage.getItem('access_token');
}

// Function to save the access token to localStorage
function saveAccessToken(accessToken) {
    localStorage.setItem('access_token', accessToken);
}

// Function to clear the access token from localStorage
function clearAccessToken() {
    localStorage.removeItem('access_token');
}

// Request interceptor to add the auth token to every request
axios.interceptors.request.use(request => {
    const accessToken = getAccessToken();
    if (accessToken) {
        request.headers.Authorization = `Bearer ${accessToken}`;
    }
    return request;
}, error => {
    return Promise.reject(error);
});

// Response interceptor to refresh the token when needed
axios.interceptors.response.use(response => response, async error => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;  // Marking the request to ensure we don't get into an infinite loop
        try {
            // Here you should call your backend API to refresh the access token using a refresh token
            const response = await axios.post('/api/token/refresh/', { refreshToken: localStorage.getItem('refresh_token') });
            const newAccessToken = response.data.accessToken;
            saveAccessToken(newAccessToken);  // Save the new access token
            axios.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;  // Update the global header
            originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;  // Update the original request
            return axios(originalRequest);  // Retry the original request with the new token
        } catch (refreshError) {
            clearAccessToken();  // Clear the access token as refresh failed
            // Redirect to login page or show an error as needed
            router.replace({ name: 'Home' });
            return Promise.reject(refreshError);
        }
    }
    return Promise.reject(error);
});

const app = createApp(App)

app.use(router)

app.mount('#app')
