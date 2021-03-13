import axios from "axios";

export default new (class AuthService {
  async getLogs() {
    const resp = axios.get(`${process.env.VUE_APP_SERVER}/logger/log`);

    return (await resp).data;
  }

  async createLog(username, status, message) {
    const resp = axios.post(`${process.env.VUE_APP_SERVER}/logger/log`, {
      username: username,
      status: status,
      message: message
    });

    return (await resp).data;
  }
})();
