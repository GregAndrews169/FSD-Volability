// src/router.js or src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import TimeSeries from './pages/TimeSeries.vue';
import StaticAnalysis from './pages/StaticAnalysis.vue';
import Correlation from './pages/Correlation.vue';
import Home from'./pages/Home.vue';
// Import other pages as needed

const routes = [
    {
        path: '/',
        name: 'TimeSeries',
        component: TimeSeries
    },
    {
        path: '/StaticAnalysis',
        name: 'StaticAnalysis',
        component: StaticAnalysis
    },
    {
        path: '/Correlation',
        name: 'Correlation',
        component: Correlation
    },

    {
        path: '/Home',
        name: 'Home',
        component: Home
    },


];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
