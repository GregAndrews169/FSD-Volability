<template>
  <div class="dashboard">
    <Sidebar />
    <div class="main-content">
      <header class="header"></header>
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './components/SideBar.vue';
</script>

<style scoped>
.dashboard {
  display: flex;
  height: 100vh;
  
  
  background: #000000;
}

.main-content {
  flex: 1;
  padding: 60px;
  overflow-y: auto;
  background: #000000;
  color: #ddd9d9;
  /* max-width: 1200px; Comment this out if you don't need a limit. */
  width: 100%;
  /* Changed from 90% to 100% */
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e1e1e1;
  width: 100%;
}
</style>
