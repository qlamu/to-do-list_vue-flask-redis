<template>
  <div>
    <h1>404</h1>
    <h2>Page not found</h2>
  </div>
</template>

<script>
export default {
  name: "NotFound",
};
</script>

<style lang="scss" scoped>
@import "@/assets/variables";

div {
  display: flex;
  align-items: baseline;
  margin: auto;
}

h1 {
  color: $red;
  font-size: 72px;
  margin: 0 1rem;
}
</style>
