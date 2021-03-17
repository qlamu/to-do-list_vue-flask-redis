<template>
  <div id="authComponent">
    <h1>{{ showRegister ? "Register" : "Login" }}</h1>
    <form @submit.prevent="showRegister ? register() : login()" class="auth">
      <input type="text" v-model="username" placeholder="Username" required />
      <input
        type="password"
        v-model="password"
        placeholder="Password"
        required
      />
      <button type="submit" v-bind:disabled="!formValidated">
        <i v-if="isFetchingAPI" class="gg-spinner"></i>
        <span v-else>{{ showRegister ? "Register" : "Login" }}</span>
      </button>
    </form>
    <p id="swapRegister" v-on:click="toggleRegisterView">
      {{
        showRegister
          ? "Already have an account ? Login"
          : "Don't have an account ? Register"
      }}
    </p>
    <div v-if="errorMessage" class="error-alert">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-alert">{{ successMessage }}</div>
  </div>
</template>

<script>
import AuthService from "@/services/AuthService";
import sha256 from "crypto-js/sha256";

export default {
  name: "Authentication",
  props: {
    showRegister: Boolean,
  },
  data() {
    return {
      username: "",
      password: "",
      isFetchingAPI: false,
      errorMessage: "",
      successMessage: "",
    };
  },
  computed: {
    formValidated: function() {
      return this.username != "" && this.password != "";
    },
  },
  methods: {
    register: function() {
      this.isFetchingAPI = true;
      this.errorMessage = "";
      this.successMessage = "";
      const resp = AuthService.register(
        this.username,
        sha256(this.password).toString()
      );
      resp
        .then((suc) => {
          this.successMessage = suc.message;
          this.$router.push("/login");
        })
        .catch((err) => (this.errorMessage = err.response.data.message))
        .finally(() => (this.isFetchingAPI = false));
    },

    login: function() {
      this.isFetchingAPI = true;
      this.errorMessage = "";
      this.successMessage = "";
      const resp = AuthService.login(
        this.username,
        sha256(this.password).toString()
      );
      resp
        .then(() => this.$router.push("/"))
        .catch((err) => (this.errorMessage = err.response.data.message))
        .finally(() => (this.isFetchingAPI = false));
    },

    toggleRegisterView: function() {
      this.$router.push(this.showRegister ? "/login" : "/signup");
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/variables";
@import "@/assets/icons";

h1 {
  margin-left: 0;
}

#authComponent {
  margin: auto;

  .auth {
    background-color: $bg-1;
    color: $fg-0;
    border-radius: 3px;
    display: inline-flex;
    flex-flow: row wrap;
    padding: 10px;

    input,
    button {
      margin: 10px;
    }

    input[type="text"],
    input[type="password"] {
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

    button {
      display: flex;
      justify-content: center;
    }
  }
}

@media (max-width: 480px) {
  #authComponent {
    min-width: 75vw;
    display: flex;
    flex-flow: column;

    .auth {
      flex-flow: column wrap;
    }
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
