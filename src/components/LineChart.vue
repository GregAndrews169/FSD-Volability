<template>
    <div class="volatility_title">
        <h2>Cryptocurrency Volatility</h2>
        <canvas ref="lineChartCanvas" width="1200" height="400"></canvas>
    </div>
</template>
  
<script>
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';
import 'chartjs-adapter-date-fns';

export default {
    props: {
        data: {
            type: Array, // array of data points, each point being { x: string, y: number }
            required: true,
        },
    },
    setup(props) {
        const lineChartCanvas = ref(null);
        let lineChart = null;

        const createOrUpdateLineChart = () => {
            if (lineChart) {
                lineChart.destroy(); // If the chart already exists, destroy it before creating a new one
            }

            const ctx = lineChartCanvas.value.getContext('2d');

            // Since your data is already in the correct format, you can directly use it in the dataset.
            const datasets = props.data.map((dataset) => ({
                label: dataset.label,  // Name of the coin
                data: dataset.data,  // Array of data points
                tension: 0.4, // Makes the line smooth
                pointRadius: 2, // Hides the points on the line
                hidden: false,
                // ... you can add more styling options specific to each dataset
            }));

            lineChart = new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: datasets, // using an array with a single dataset
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            grid: { color: '#37474F', },
                            type: 'time',
                            time: {
                                displayFormats: {
                                    quarter: 'MMM YYYY'
                                }
                            }
                        },
                        y: {
                            grid: { color: '#37474F', },
                            beginAtZero: true,
                        }
                    },
                    legend: { display: true },


                    // ... other options as needed
                },
            });
        };

        onMounted(() => {
            createOrUpdateLineChart();
        });

        watch(() => props.data, () => {
            createOrUpdateLineChart(); // When the data prop changes, the chart will update
        }, { deep: true });

        return {
            lineChartCanvas,
        };
    },
};
</script>

  
<style scoped>
/* Styles specific to the Sidebar component */

.volatility_title h2 {
    color: #ddd9d9;
}
</style>
  