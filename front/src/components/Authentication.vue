<template>
  <div class="container">
    <h2>Register</h2>
    <form class="auth">
      <input type="text" v-model="username" placeholder="Username" />
      <input type="password" v-model="password" placeholder="Password"  />
      <input type="submit" value="Register" v-if="isRegister" v-on:click.prevent="register" />
      <input type="submit" value="Login" v-else v-on:click.prevent="login" />
    </form>
    <p id="swapRegister" v-on:click="toggleRegisterView">
      {{
        isRegister
          ? "Already have an account ? Login"
          : "Don't have an account ? Register"
      }}
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import AuthService from "@/services/AuthService";

@Component
export default class Authentication extends Vue {
  private isRegister = true;
  private username = "";
  private password = "";

  register() {
    console.log("register");
    const resp = AuthService.register(this.username, this.password);
    resp.then((d) => console.log(d));
  }

  login() {
    console.log("login");
    const resp = AuthService.login(this.username, this.password);
    resp.then((d) => console.log(d));
  }

  toggleRegisterView() {
    this.isRegister = !this.isRegister;
  }
}
</script>

<style lang="scss">
@import "@/assets/variables";

.auth {
  background-color: $bg-1;
  color: $fg-0;
  border-radius: 3px;
  display: inline-flex;
  padding: 10px;

  * {
    margin: 10px;
  }

  input[type=text], input[type=password] {
    background-color: $bg-2;
    color: $fg-0;
    border: 1px solid $bg-3;
    border-radius: 3px;
    padding: 10px;
  }

  input:focus {
    outline: none;
    border-color: $accent;
  }
}

#swapRegister {
  font-size: 0.85rem;
  color: $accent;
  transition: color 0.33s ease;
  cursor: pointer;
}

#swapRegister:hover {
  color: #81a1c1;
}
</style>
