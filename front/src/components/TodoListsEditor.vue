<template>
  <div>
    <h1>
      <span v-if="list">{{ list.title }}</span>
      <span v-else>Select a list to continue</span>
      <i v-if="isFetchingAPI" class="gg-spinner"></i>
    </h1>
    <transition name="scale">
      <div v-if="errorMessage" class="error-alert">{{ errorMessage }}</div>
    </transition>
    <div class="inputWrapper">
      <input
        type="text"
        v-model="searchContent"
        placeholder="Search or Create a new todo"
        v-on:keydown.ctrl.enter="createTodo"
      />
    </div>
    <transition name="scale">
      <button
        v-if="searchContent"
        v-on:click="createTodo"
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
      <li v-for="todo in sortedTodos" :key="todo.todo_id">
        <div class="list-item" v-if="todo.todo_id != editedTodoID">
          <div>
            <button
              v-if="todo.is_done == 1"
              class="done-todo"
              @click="toggleIsDone(todo.todo_id)"
            ></button>
            <button
              v-else
              class="undone-todo"
              @click="toggleIsDone(todo.todo_id)"
            ></button>
            <span>{{ todo.description }}</span>
          </div>
          <div>
            <button id="editBtn" @click="toggleEdit(todo.todo_id)"></button>
            <button id="deleteBtn" @click="deleteTodo(todo.todo_id)"></button>
          </div>
        </div>
        <div v-else class="list-item">
          <textarea type="text" v-model="editedTodo.description" v-on:keydown.ctrl.enter="patchEditedTodo" />
          <button id="confirmBtn" @click="patchEditedTodo"></button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import ListsService from "@/services/ListsService";
import TodosService from "@/services/TodosService";

export default {
  name: "TodoListsEditor",
  data() {
    return {
      list: null,
      todos: [],
      searchContent: "",
      isFetchingAPI: false,
      errorMessage: "",
      editedTodoID: null,
    };
  },
  created() {
    this.fetchTodoFromRoute();
  },
  computed: {
    sortedTodos: function() {
      return this.todos
        .filter((todo) =>
          todo.description
            .toLowerCase()
            .includes(this.searchContent.toLowerCase())
        )
        .sort((a, b) => a.todo_id - b.todo_id);
    },
    editedTodo: function() {
      return this.todos.find((todo) => todo.todo_id == this.editedTodoID);
    },
  },
  methods: {
    fetchTodoFromRoute() {
      if (this.$route.params.list_id) {
        this.isFetchingAPI = true;
        this.errorMessage = "";
        let resp = ListsService.getList(this.$route.params.list_id);
        resp
          .then((suc) => (this.list = suc.data.list))
          .catch(
            (err) =>
              (this.errorMessage =
                err.response?.data.message || "Error: Could not reach server")
          )
          .finally(() => (this.isFetchingAPI = false));

        resp = TodosService.getTodos(this.$route.params.list_id);
        resp
          .then((suc) => (this.todos = suc.data.todos))
          .catch(
            (err) =>
              (this.errorMessage =
                err.response?.data.message || "Error: Could not reach server")
          )
          .finally(() => (this.isFetchingAPI = false));
      }
    },

    createTodo() {
      this.isFetchingAPI = true;
      this.errorMessage = "";
      const resp = TodosService.createTodo(this.list.list_id, this.searchContent);
      resp
        .then((suc) => {
          this.todos.push({
            description: this.searchContent,
            is_done: 0,
            todo_id: suc.data.todo_id,
          });
          this.searchContent = "";
        })
        .catch(
          (err) =>
            (this.errorMessage =
              err.response?.data.message || "Error: Could not reach server")
        )
        .finally(() => (this.isFetchingAPI = false));
    },

    deleteTodo(todoID) {
      this.isFetchingAPI = true;
      this.errorMessage = "";
      const removedTodo = this.todos.find((todo) => todo.todo_id == todoID);
      this.todos.splice(this.todos.indexOf(removedTodo), 1);
      const resp = TodosService.deleteTodo(this.list.list_id, todoID);
      resp
        .catch((err) => {
          this.errorMessage =
            err.response?.data.message || "Error: Could not reach server";
          this.todos.push(removedTodo); // Could not delete
        })
        .finally(() => (this.isFetchingAPI = false));
    },

    toggleEdit(todoID) {
      this.editedTodoID = todoID;
    },

    patchEditedTodo() {
      this.isFetchingAPI = true;
      this.errorMessage = "";
      const resp = TodosService.patchTodo(
        this.list.list_id,
        this.editedTodo.todo_id,
        this.editedTodo.description,
        this.editedTodo.is_done
      );
      resp
        .catch((err) => {
          this.errorMessage =
            err.response?.data.message || "Error: Could not reach server";
        })
        .finally(() => (this.isFetchingAPI = false));

      this.editedTodoID = null;
    },

    toggleIsDone(todoID) {
      this.isFetchingAPI = true;
      this.errorMessage = "";
      const patchedTodo = this.todos.find((todo) => todo.todo_id == todoID);
      patchedTodo.is_done = patchedTodo.is_done == 1 ? 0 : 1;
      const resp = TodosService.patchTodo(
        this.list.list_id,
        patchedTodo.todo_id,
        patchedTodo.description,
        patchedTodo.is_done
      );
      resp
        .catch((err) => {
          this.errorMessage =
            err.response?.data.message || "Error: Could not reach server";
            patchedTodo.is_done = patchedTodo.is_done == "1" ? "0" : "1"; // Revert
        })
        .finally(() => (this.isFetchingAPI = false));
    },
  },
  watch: {
    "$route.params.list_id": {
      handler: function() {
        this.fetchTodoFromRoute();
      },
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/variables";

.list-item {
  margin-top: 0;
}

ul {
  padding: 1rem;
}

ul li:hover {
  background-color: $bg-1;
}

ul li:not(:last-child) {
  border-bottom: 1px solid $bg-2;
}

.inputWrapper {
  box-sizing: border-box;
  width: 100%;
  background: $bg-1;
  display: flex;

  input[type="text"] {
    background-color: $bg-1;
    color: $fg-0;
    border-width: 1px 0 1px 0;
    border-color: $bg-3;
    border-style: solid;
    padding: 10px;
    box-sizing: border-box;
    flex: 1;
  }

  input:focus {
    outline: none;
    border-color: $accent;
  }
}
</style>
