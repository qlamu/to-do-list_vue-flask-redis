<template>
  <div class="grid" v-bind:class="{ mobileSwap: $route.path == '/' }">
    <router-link class="mobileNav" to="/" v-show="$route.path != '/'" />
    <TodoListsSidenav v-on:refreshTodosPanel="refreshProp = !refreshProp" class="sidenav" />
    <TodoListsEditor class="content" :refresh="refreshProp" />
  </div>
</template>

<script>
import TodoListsSidenav from "@/components/TodoListsSidenav";
import TodoListsEditor from "@/components/TodoListsEditor";

export default {
  name: "Home",
  components: {
    TodoListsSidenav,
    TodoListsEditor,
  },
  data() {
    return {
      refreshProp: false
    }
  }
};
</script>
