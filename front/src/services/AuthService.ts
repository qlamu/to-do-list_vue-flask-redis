import { DefaultResponse } from "@/models/DefaultResponse";
import { Login } from "@/models/models";
import axios from "axios";

export default new (class AuthService {
  async register(username: string, password: string) {
    const resp = await axios.post(
      "http://localhost:5000/account",
      {
        username: username,
        password: password,
      },
      { headers: { "Content-Type": "application/json" } }
    );

    return resp.data;
  }

  async login(username: string, password: string) {
    const resp = axios.post("http://localhost:5000/login", {
      username: username,
      password: password,
    });

    const json: DefaultResponse<Login> = (await resp).data;

    if (json.data?.hasOwnProperty("jwt")) {
      axios.defaults.headers.common = {
        Authorization: `Bearer ${json.data.jwt}`,
      };
    }

    return json;
  }
})();
