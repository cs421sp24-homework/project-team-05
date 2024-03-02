const VITE_SECHAND_BACKEND_API_ENTRY = "https://oose-project-65116e9428b0.herokuapp.com/"
const VITE_LOCAL_HOST = "http://localhost:8000/"
const DEV = true
const HTTP_PREFIX = DEV ? VITE_LOCAL_HOST : VITE_SECHAND_BACKEND_API_ENTRY


export default  HTTP_PREFIX