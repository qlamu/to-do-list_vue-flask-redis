import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";

Vue.config.productionTip = false;

import "@/assets/styles.scss";

axios.defaults.headers.common = {
  "Content-Type": "application/json",
};
axios.defaults.timeout = 10000;
axios.interceptors.response.use(
  function(response) {
    return response;
  },
  function(error) {
    if (error.response?.status == 401) {
      console.log("LOGGED OUT");
      axios.defaults.headers.common = {
        Authorization: "",
      };
      router.push("/login");
    }
    return Promise.reject(error);
  }
);
if(localStorage.getItem("jwt") !== null) {
  axios.defaults.headers.common = {
    Authorization: `Bearer ${localStorage.getItem("jwt")}`,
  };
}

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
