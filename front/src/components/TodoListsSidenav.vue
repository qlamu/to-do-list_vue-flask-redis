<template>
  <div>
    <h1>Lists</h1>
    <input
      type="text"
      v-model="searchContent"
      placeholder="Search or Create a new list"
      v-on:keydown.ctrl.enter="createList"
    />
    <button v-if="canCreate" v-on:click="createList">
      <i v-if="isFetchingAPI" class="gg-spinner"></i>
      <div v-else>
        <span>Create {{ searchContent }}</span>
        <span><kbd>CTRL</kbd>+<kbd>ENTER</kbd></span>
      </div>
    </button>
    <ul>
      <li v-for="list in sortedLists" :key="list.message">
        {{ list.title }}
      </li>
    </ul>
  </div>
</template>

<script>
import ListsService from "@/services/ListsService";

export default {
  name: "TodoLists",
  data() {
    return {
      searchContent: "",
      lists: [
        {
          title:
            "One very long title with a huge description that serve no purpose",
        },
        {
          title: "2",
        },
        {
          title: "3",
        },
        {
          title: "4",
        },
      ],
      isFetchingAPI: false,
      errorMessage: "",
    };
  },
  created() {
    this.fetchLists();
  },
  computed: {
    sortedLists: function() {
      return this.lists
        .filter((list) =>
          list.title.toLowerCase().includes(this.searchContent.toLowerCase())
        )
        .sort((a, b) => a.list_id - b.list_id);
    },
    canCreate: function() {
      return (
        this.searchContent != "" &&
        this.lists.find((list) => list.title == this.searchContent) == undefined
      );
    },
  },
  methods: {
    fetchLists() {
      this.isFetchingAPI = true;
      const resp = ListsService.getLists();
      resp
        .then((suc) => (this.lists = suc.data.lists))
        .catch((err) => (this.errorMessage = err.response.data.message))
        .finally(() => (this.isFetchingAPI = false));
    },

    createList() {
      this.isFetchingAPI = true;
      const resp = ListsService.createList(this.searchContent);
      resp
        .then(() => {
          this.searchContent = "";
          this.fetchLists();
        })
        .catch((err) => (this.errorMessage = err.response.data.message))
        .finally(() => (this.isFetchingAPI = false));
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/variables";
@import "@/assets/icons";

input[type="text"] {
  background-color: $bg-2;
  color: $fg-0;
  border-width: 1px 0 1px 0;
  border-color: $bg-3;
  border-style: solid;
  padding: 10px;
  box-sizing: border-box;
  width: 100%;
}

input:focus {
  outline: none;
  border-color: $accent;
}

button {
  width: 100%;
  border-radius: 0;
  display: flex;
  justify-content: center;

  div {
    display: flex;
    flex-wrap: wrap;
    text-align: center;
    flex-direction: column;
  }
}
</style>
