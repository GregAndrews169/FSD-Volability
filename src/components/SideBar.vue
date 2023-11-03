<template>
    <aside class="sidebar">
        <div>
            <img class="logo" src="../assets/LogoVol.png" alt="Your Logo" />
        </div>
        <ul class="button-list">
            <li class="link" :class="{ active: $route.path === '/' }">
                <router-link to="/">
                    <button class="button-style">Home</button>
                </router-link>
            </li>
            <li class="link" :class="{ active: $route.path === '/PnL' }">
                <router-link to="/PnL">
                    <button class="button-style">Profit & Loss Analysis </button>
                </router-link>
            </li>
            <li class="link" :class="{ active: $route.path === '/TimeSeries' }">
                <router-link to="/TimeSeries">
                    <button class="button-style">Time Series Analysis</button>
                </router-link>
            </li>
            <li class="link" :class="{ active: $route.path === '/StaticAnalysis' }">
                <router-link to="/StaticAnalysis">
                    <button class="button-style">Static Analysis</button>
                </router-link>
            </li>
            <li class="link" :class="{ active: $route.path === '/Correlation' }">
                <router-link to="/Correlation">
                    <button class="button-style">Correlation</button>
                </router-link>
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
    margin-right: 8px;
    border-radius: 10px;
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
    color: #e62e2e !important;
}

/* Styling for the active link */
.sidebar .active a {
    color: #df1212 !important;
}

.logo {
    padding-left: 15px;

}

.button-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.button-style {
    background-color: black;
    color: white;
    display: block;
    width: 100%;
    padding: 10px;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.2s, border-color 0.2s, color 0.2s;
}

.button-style.active {
    background-color: #9746D6;
    /* Purple background when active */
    color: white;
    border: 1px solid #9746D6;
    /* Purple border color when active */
}

.button-style:hover {
    background-color: #9746D6;
    color: white;
    border: 1px solid #9746D6;
    /* Purple border color on hover and when active */
}
</style>
