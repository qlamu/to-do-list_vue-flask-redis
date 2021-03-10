<template>
  <div class="home">
    <Authentication/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Authentication from '@/components/Authentication.vue'; // @ is an alias to /src

@Component({
  components: {
    Authentication
  },
})
export default class Home extends Vue {}
</script>
