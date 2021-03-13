import axios from "axios";

export default new (class AuthService {
  async register(username, password) {
    const resp = axios.post(`${process.env.VUE_APP_SERVER}/account`, {
      username: username,
      password: password,
    });

    return (await resp).data;
  }

  async login(username, password) {
    const resp = axios.post(`${process.env.VUE_APP_SERVER}/login`, {
      username: username,
      password: password,
    });

    const json = (await resp).data;
    if (json.data?.jwt) {
      axios.defaults.headers.common = {
        Authorization: `Bearer ${json.data.jwt}`,
      };
      localStorage.setItem("jwt", json.data.jwt);
    }

    return json;
  }

  signOut() {
    axios.defaults.headers.common = {};
    localStorage.removeItem("jwt");
  }

})();
