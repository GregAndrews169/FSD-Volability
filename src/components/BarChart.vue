<template>
    <div class="bar_chart_title">
        <canvas ref="barChartCanvas" width="970" height="400"></canvas>
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
        const barChartCanvas = ref(null);
        let barChart;

        const createOrUpdateBarChart = () => {
            if (barChart) {
                barChart.destroy();
            }

            const ctx = barChartCanvas.value.getContext('2d');




            const datasets = props.data.map(coin => ({
                label: coin.label,
                data: coin.data,
                backgroundColor: coin.backgroundColor,
            }));



            barChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ["Coins"],
                    datasets: datasets,
                },
                options: {
                    scales: {
                        y: { beginAtZero: true },
                    },
                    responsive: false,
                    maintainAspectRatio: false,
                },
            });
        };

        onMounted(createOrUpdateBarChart);
        watch(() => props.data, createOrUpdateBarChart, { deep: true });

        return { barChartCanvas };
    },
};
</script>

<style scoped>
.bar_chart_title h2 {
    color: #ddd9d9;
}
</style>
