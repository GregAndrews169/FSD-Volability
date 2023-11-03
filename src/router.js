// src/router.js or src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import TimeSeries from './pages/TimeSeries.vue';
import StaticAnalysis from './pages/StaticAnalysis.vue';
import Correlation from './pages/Correlation.vue';
import PnL from './pages/PnL.vue';
import Home from './pages/Home.vue';
// Import other pages as needed

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/PnL',
        name: 'PnL',
        component: PnL
    },
    {
        path: '/TimeSeries',
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
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
