<template>
  <div class="grid">
    <TodoListsSidenav class="sidenav" />
    <div class="content">
      <h1>Todo list manager</h1>
      <img
        src="@/assets/images/undraw_No_data_re_kwbl.svg"
        alt=""
        width="200rem"
      />
    </div>
  </div>
</template>

<script>
import TodoListsSidenav from "@/components/TodoListsSidenav";

export default {
  name: "Home",
  components: {
    TodoListsSidenav,
  },
};
</script>
