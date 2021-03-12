<template>
  <div>
    <h1>
      <span>Lists</span>
      <i v-if="isFetchingAPI" class="gg-spinner"></i>
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
      <button v-if="canCreate" v-on:click="createList" class="createListButton">
        <i v-if="isFetchingAPI" class="gg-spinner"></i>
        <div v-else>
          <span>Create {{ searchContent }}</span>
          <span><kbd>CTRL</kbd>+<kbd>ENTER</kbd></span>
        </div>
      </button>
    </transition>
    <ul>
      <li
        v-for="list in sortedLists"
        :key="list.list_id"
        @click="$router.push('/' + list.list_id)"
      >
        <div
          v-if="list.list_id != editedListID"
          v-bind:class="{ active: $route.params.list_id == list.list_id }"
        >
          <span>{{ list.title }}</span>
          <button id="editBtn" @click="toggleEdit(list.list_id)">
            <i class="gg-pen"></i>
          </button>
          <button id="deleteBtn" @click="deleteList(list.list_id)">
            <i class="gg-trash-empty"></i>
          </button>
        </div>
        <div v-else>
          <input type="text" v-model="editedList.title" />
          <button id="confirmBtn" @click="patchEditedList">V</button>
        </div>
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
      lists: [],
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
        .catch((err) => {
          this.errorMessage =
            err.response?.data.message || "Error: Could not reach server";
          this.lists.push(removedList); // Could not delete
        })
        .finally(() => (this.isFetchingAPI = false));
    },

    toggleEdit(listID) {
      this.editedListID = listID;
    },

    patchEditedList() {
      this.isFetchingAPI = true;
      const resp = ListsService.patchList(
        this.editedList.list_id,
        this.editedList.title
      );
      resp
        .catch((err) => {
          this.errorMessage =
            err.response?.data.message || "Error: Could not reach server";
        })
        .finally(() => (this.isFetchingAPI = false));

      this.editedListID = null;
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

.createListButton {
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

ul {
  list-style-type: none;
  padding: 0;
}

ul li div {
  padding-left: 0.8rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  padding: 10px;

  span {
    flex-grow: 1;
  }

  button {
    background: transparent;
    color: $fg-2;
    border-radius: 0;
    align-self: stretch;
    margin: 4px;
  }

  button:hover {
    background: $bg-3;
    color: $fg-0;
  }
}
ul li:hover {
  background-color: $bg-2;
  cursor: pointer;
}

#editBtn {
  mask: url("../assets/images/pen_icon.svg") no-repeat center;
  -webkit-mask: url("../assets/images/pen_icon.svg") no-repeat center;
  mask-size: contain;
  background-color: $fg-2;
}

#editBtn:hover {
  background-color: $accent;
}

#deleteBtn {
  mask: url("../assets/images/trash_icon.svg") no-repeat center;
  -webkit-mask: url("../assets/images/trash_icon.svg") no-repeat center;
  mask-size: contain;
  background-color: $fg-2;
}

#deleteBtn:hover {
  background-color: $red;
}

#confirmBtn {
  mask: url("../assets/images/check_icon.svg") no-repeat center;
  -webkit-mask: url("../assets/images/check_icon.svg") no-repeat center;
  mask-size: contain;
  background-color: $fg-2;
}

#confirmBtn:hover {
  background-color: $accent;
}

.active {
  border-left: 3px solid $accent;
  color: $accent;
}
</style>
