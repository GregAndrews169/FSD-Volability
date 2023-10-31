import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import CsvImporter from './components/CsvImporter.vue';
import ScatterPlot from './components/ScatterPlot.vue'; // Import the ScatterPlot component
import LineChart from './components/LineChart.vue';// Import the BarChart component
import router from './router'; // Or './router/index.js' based on your file structure

const app = createApp(App);

// Register the CsvImporter component
app.component('CsvImporter', CsvImporter);
app.component('ScatterPlot', ScatterPlot);
app.use(router).mount('#app');
