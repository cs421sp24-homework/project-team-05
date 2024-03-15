// import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import { createApp, ref } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import '@popperjs/core'
import 'bootstrap/dist/js/bootstrap.bundle.min.js';


const HTTP_PREFIX = import.meta.env.VITE_HOST;

// Response interceptor to refresh the token when needed
axios.interceptors.response.use(response => response, async error => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry && !originalRequest.url.includes('api/token/refresh/')) {
        originalRequest._retry = true;  // Marking the request to ensure we don't get into an infinite loop
        try {
            // Here you should call your backend API to refresh the access token using a refresh token
            const refreshToken = localStorage.getItem('refresh_token');
            const response = await axios.post(HTTP_PREFIX + 'api/token/refresh/', { "refresh": refreshToken });
            const newAccessToken = response.data.access;
            localStorage.setItem('access_token', newAccessToken);
            axios.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;  // Update the global header
            originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;  // Update the original request
            console.log("new auth");
            return axios(originalRequest);  // Retry the original request with the new token
        } catch (refreshError) {
            axios.defaults.headers.common['Authorization'] = undefined;
            localStorage.clear();
            // console.log("refresh error", refreshError);
            router.replace({ name: 'Home' });
            return Promise.reject(refreshError);
        }
    }
    axios.defaults.headers.common['Authorization'] = undefined;
    localStorage.clear();
    router.replace({ name: 'Home' });
    // console.log("other error", error);
    return Promise.reject(error);
});

const app = createApp(App)

app.use(router)

app.mount('#app')
