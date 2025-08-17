import axios from "axios";

const client = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: false,
  timeout: 30000,
});


client.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err.response) {
      console.error("API error:", err.response.status, err.response.data);
    } else {
      console.error("Network/API error:", err.message);
    }
    return Promise.reject(err);
  }
);

export default client;
