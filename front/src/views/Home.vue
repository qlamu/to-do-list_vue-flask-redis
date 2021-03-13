<template>
  <div class="grid">
    <TodoListsSidenav class="sidenav" />
    <TodoListsEditor class="content" />
  </div>
</template>

<script>
import TodoListsSidenav from "@/components/TodoListsSidenav";
import TodoListsEditor from "@/components/TodoListsEditor";

export default {
  name: "Home",
  components: {
    TodoListsSidenav,
    TodoListsEditor
  },
};
</script>
