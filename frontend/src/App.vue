<script setup>
  import { RouterView } from 'vue-router';
  import NavBar from './components/ui/NavBar.vue';
</script>

<template>
  <NavBar />
  <div class="container">
    <RouterView />
  </div>
</template>
