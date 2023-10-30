<template>
    <aside class="sidebar">
        <div>
            <img class= "logo" src="../assets/LogoVol.png" alt="Your Logo" />
        </div>
        <ul>
            <li class="link" :class="{ active: $route.path === '/' }">
                <router-link to="/">Time Series Analysis</router-link>
            </li>
            <li class="link" :class="{ active: $route.path === '/StaticAnalysis' }">
                <router-link to="/StaticAnalysis">Static Analysis</router-link>
            </li>
            <li class="link" :class="{ active: $route.path === '/Correlation' }">
                <router-link to="/Correlation">Correlation</router-link>
            </li>
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
    background-color: #000000;
    color: #b5b5c3;
    width: 200px;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar h3 {
    color: #fff;
}

.sidebar li {
    margin-top: 20px;
    cursor: pointer;
    color: #fff;
}

.sidebar .link a {
    color: #b5b5c3 !important;
    text-decoration: none !important;
}

/* Modify the link color when hovered */
.sidebar .link a:hover {
    color: #fff !important;
}

/* Styling for the active link */
.sidebar .active a {
    color: #fff !important;
}

.logo{
    padding-left: 30px;

}
</style>
