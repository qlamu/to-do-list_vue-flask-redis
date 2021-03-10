import axios from "axios";

export default new (class AuthService {
  async register(username, password) {
    const resp = axios.post(
      "http://localhost:5000/account",
      {
        username: username,
        password: password,
      },
      { headers: { "Content-Type": "application/json" } }
    );

    return (await resp).data;
  }

  async login(username, password) {
    const resp = axios.post("http://localhost:5000/login", {
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
