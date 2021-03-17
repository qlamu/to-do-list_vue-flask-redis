<template>
  <div>
    <h1>
      <div>
        <span ref="test">Lists</span>
        <i v-if="isFetchingAPI" class="gg-spinner"></i>
      </div>
      <button class="signout" @click="signOut" title="Sign out"></button>
    </h1>
    <transition name="scale">
      <div v-if="errorMessage" class="error-alert">{{ errorMessage }}</div>
    </transition>
    <input
      type="text"
      v-model="searchContent"
      placeholder="Search or Create a new list"
      v-on:keydown.ctrl.enter="createList"
    />
    <transition name="scale">
      <button
        v-if="canCreate"
        v-on:click="createList"
        class="create-item-button"
      >
        <i v-if="isFetchingAPI" class="gg-spinner"></i>
        <div v-else>
          <span>Create {{ searchContent }}</span>
          <span><kbd>CTRL</kbd>+<kbd>ENTER</kbd></span>
        </div>
      </button>
    </transition>
    <ul>
      <li v-for="list in sortedLists" :key="list.list_id">
        <div
          v-if="list.list_id != editedListID"
          class="list-item"
          v-bind:class="{ active: $route.params.list_id == list.list_id }"
        >
          <span @click="changeSelection(list.list_id)">{{ list.title }}</span>
          <button
            id="editBtn"
            @click="toggleEdit(list.list_id)"
            title="Edit"
          ></button>
          <button
            id="deleteBtn"
            @click="deleteList(list.list_id)"
            title="Delete"
          ></button>
        </div>
        <div v-else class="list-item editActive">
          <textarea
            type="text"
            v-model="editedList.title"
            v-on:keydown.ctrl.enter="patchEditedList"
            :ref="`titleTextarea${list.list_id}`"
          />
          <button
            id="confirmBtn"
            @click="patchEditedList"
            title="Save"
          ></button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import ListsService from "@/services/ListsService";
import AuthService from "@/services/AuthService";

export default {
  name: "TodoLists",
  data() {
    return {
      lists: [],
      searchContent: "",
      isFetchingAPI: false,
      errorMessage: "",
      editedListID: null,
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
    editedList: function() {
      return this.lists.find((list) => list.list_id == this.editedListID);
    },
  },
  methods: {
    fetchLists() {
      this.isFetchingAPI = true;
      this.errorMessage = "";
      const resp = ListsService.getLists();
      resp
        .then((suc) => (this.lists = suc.data.lists))
        .catch(
          (err) =>
            (this.errorMessage =
              err.response?.data.message || "Error: Could not reach server")
        )
        .finally(() => (this.isFetchingAPI = false));
    },

    createList() {
      this.isFetchingAPI = true;
      this.errorMessage = "";
      const resp = ListsService.createList(this.searchContent);
      resp
        .then(() => {
          this.searchContent = "";
          this.fetchLists();
        })
        .catch(
          (err) =>
            (this.errorMessage =
              err.response?.data.message || "Error: Could not reach server")
        )
        .finally(() => (this.isFetchingAPI = false));
    },

    deleteList(listID) {
      this.isFetchingAPI = true;
      this.errorMessage = "";
      const removedList = this.lists.find((list) => list.list_id == listID);
      this.lists.splice(this.lists.indexOf(removedList), 1);
      const resp = ListsService.deleteList(listID);
      resp
        .then(() => {
          if (this.$route.params.list_id == listID) {
            this.$emit("deleteActiveList");
            this.$router.push("/");
          }
        })
        .catch((err) => {
          this.errorMessage =
            err.response?.data.message || "Error: Could not reach server";
          this.lists.push(removedList); // Could not delete
        })
        .finally(() => (this.isFetchingAPI = false));
    },

    toggleEdit(listID) {
      this.editedListID = listID;
      this.$nextTick(() => {
        this.$refs[`titleTextarea${listID}`][0].focus();
      });
    },

    patchEditedList() {
      this.isFetchingAPI = true;
      const resp = ListsService.patchList(
        this.editedList.list_id,
        this.editedList.title
      );
      resp
        .then(() => this.$emit("refreshTodosPanel"))
        .catch((err) => {
          this.errorMessage =
            err.response?.data.message || "Error: Could not reach server";
        })
        .finally(() => (this.isFetchingAPI = false));

      this.editedListID = null;
    },

    changeSelection(listID) {
      if (this.$route.params.list_id != listID) this.$router.push("/" + listID);
    },

    signOut() {
      AuthService.signOut();
      this.$router.push("/login");
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/variables";
@import "@/assets/icons";

input[type="text"] {
  background-color: $bg-2;
  width: 100%;
}

.active {
  border-left: 3px solid $accent;
  color: $accent;
}

.editActive {
  background-color: $bg-2;
}
</style>
