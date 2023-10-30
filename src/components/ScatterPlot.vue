<template>
    <div>
        <h2>Scatter Plot</h2>
        <canvas ref="scatterPlotCanvas" width="400" height="200"></canvas>
    </div>
</template>
  
<script>
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

export default {
    props: {
        data: {
            type: Array,
            required: true,
        },
    },
    setup(props) {
        const scatterPlotCanvas = ref(null);
        let scatterChart = null;

        // Create or update the scatter plot
        const createOrUpdateScatterPlot = () => {
            if (scatterChart) {
                scatterChart.destroy();
            }

            const ctx = scatterPlotCanvas.value.getContext('2d');
            const dataset = {
                label: 'Price vs. City MPG',
                data: props.data.map((d) => ({ x: d.price, y: d['city-mpg'] })),
                pointRadius: 5,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                showLine: false,
            }

            const dataset2 = {
                label: 'Price vs. Highway MPG',
                data: props.data.map((d) => ({ x: d.price, y: d['highway-mpg'] })),
                pointRadius: 5,
                borderColor: 'rgba(175, 92, 92, 1)',
                borderWidth: 1,
                showLine: false,
            };

            scatterChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [dataset, dataset2],
                },
                options: {
                    scales: {
                        x: {
                            type: 'linear',
                            position: 'bottom',
                            beginAtZero: true,
                        },
                        y: {
                            type: 'linear',
                            beginAtZero: true,
                        },
                    },
                },
            });
        };

        onMounted(() => {
            createOrUpdateScatterPlot();
        });

        watch(() => props.data, () => {
            // Re-render the scatter plot when data changes
            createOrUpdateScatterPlot();
        }, { deep: true });

        return {
            scatterPlotCanvas,
        };
    },
};

</script>

