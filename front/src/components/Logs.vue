<template>
  <div style="width: 100%">
    <h1>
      <span>Logs</span>
      <i v-if="isFetchingAPI" class="gg-spinner"></i>
    </h1>
    <table>
      <tr>
        <th>Username</th>
        <th>Status</th>
        <th>Message</th>
      </tr>
      <tr
        v-for="(log, index) in logs"
        :key="index"
       
      >
        <td  v-bind:class="[ log.status >= 199 && log.status < 300 ? 'borderGreen' : 'borderRed']">{{ log.username }}</td>
        <td>{{ log.status }}</td>
        <td>{{ log.message }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import LogsService from "@/services/LogsService";

export default {
  name: "Logs",
  data() {
    return {
      logs: [],
      isFetchingAPI: false,
    };
  },
  created() {
    this.getLogs();
    setInterval(this.getLogs, 2000);
  },
  methods: {
    getLogs() {
      this.isFetchingAPI = true;
      const resp = LogsService.getLogs();
      resp
        .then((suc) => (this.logs = suc.data.logs))
        .catch(
          (err) =>
            (this.errorMessage =
              err.response?.data.message || "Error: Could not reach server")
        )
        .finally(() => (this.isFetchingAPI = false));
    },
  },
};
</script>

<style lang="scss">
@import "@/assets/variables";
table {
  width: 100%;
}

tr,
td {
  padding: 1rem;
  text-align: left;
}

.borderGreen {
  border-left: 3px solid $green;
}

.borderRed {
  border-left: 3px solid $red;
}
</style>
