<template>
    <aside class="sidebar">
        <h3>DASHBOARD</h3>
        <ul>
            <li>CHART TYPE</li>
            <router-link to="/" tag="li" class="link" active-class="active">Time Series Analysis</router-link>
            <li class="active">Static Analysis</li>
            <li class="active">Correlation</li>
            <!-- Add more chart types as needed -->
        </ul>
    </aside>
</template>
  
<script>
export default {
    name: "Sidebar",
    // You can add props, data, computed properties, methods, etc. if needed
};
</script>
  
<style scoped>
/* Styles specific to the Sidebar component */
.sidebar {
    background-color: #4d824de4;
    color: #b5b5c3;
    width: 240px;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar h3 {
    color: #fff;
}

.sidebar li {
    margin-top: 20px;
    cursor: pointer;
}

.sidebar .active {
    color: #fff;
}
</style>
  