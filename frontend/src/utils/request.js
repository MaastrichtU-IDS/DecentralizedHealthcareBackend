import axios from "axios";

const BASE_API = "http://localhost:8000"

const service = axios.create(
    {
        baseURL: BASE_API,
        timeout: 60000000
    }
)

service.defaults.headers.post['Content-Type'] = 'application/json'
service.defaults.headers.get['Content-Type'] = 'application/json'
export default service