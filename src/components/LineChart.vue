<template>
    <div class="volatility_title">

        <canvas ref="lineChartCanvas" width="970" height="400"></canvas>
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
        initialHidden: {
            type: Boolean,
            default: true, // hide/not-hide legend
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

            const datasets = props.data.map((dataset) => ({
                label: dataset.label,
                data: dataset.data,
                tension: 0.4,
                pointRadius: 2,
                hidden: props.initialHidden,
            }));

            lineChart = new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: datasets,
                },
                options: {
                    responsive: false,
                    maintainAspectRatio: false,
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
                },
            });
        };

        onMounted(() => {
            createOrUpdateLineChart();
        });

        watch(() => props.data, () => {
            createOrUpdateLineChart();
        }, { deep: true });

        return {
            lineChartCanvas,
        };
    },
};
</script>

<style scoped></style>
