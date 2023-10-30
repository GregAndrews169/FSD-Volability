import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import CsvImporter from './components/CsvImporter.vue';
import ScatterPlot from './components/ScatterPlot.vue'; // Import the ScatterPlot component
import LineChart from './components/LineChart.vue';// Import the BarChart component


const app = createApp(App);

// Register the CsvImporter component
app.component('CsvImporter', CsvImporter);
app.component('ScatterPlot', ScatterPlot);
// app.component('BarChart', BarChart);

app.mount('#app');
