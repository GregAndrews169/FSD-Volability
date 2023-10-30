// src/router.js or src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import TimeSeries from './pages/TimeSeries.vue';

// Import other pages as needed

const routes = [
    {
        path: '/',
        name: 'TimeSeries',
        component: TimeSeries
    },
    // ... other routes go here
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
