import axios from "axios";
import { server } from "@/services/config";

export default new (class AuthService {
  async getLogs() {
    const resp = axios.get(`${server}/logger/log`);

    return (await resp).data;
  }

  async createLog(username, status, message) {
    const resp = axios.post(`${server}/logger/log`, {
      username: username,
      status: status,
      message: message
    });

    return (await resp).data;
  }
})();
