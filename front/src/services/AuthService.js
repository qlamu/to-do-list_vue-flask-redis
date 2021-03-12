import axios from "axios";
import { server } from "@/services/config";

export default new (class AuthService {
  async register(username, password) {
    const resp = axios.post(`${server}/account`, {
      username: username,
      password: password,
    });

    return (await resp).data;
  }

  async login(username, password) {
    const resp = axios.post(`${server}/login`, {
      username: username,
      password: password,
    });

    const json = (await resp).data;
    if (json.data?.jwt) {
      axios.defaults.headers.common = {
        Authorization: `Bearer ${json.data.jwt}`,
      };
    }

    return json;
  }
})();
