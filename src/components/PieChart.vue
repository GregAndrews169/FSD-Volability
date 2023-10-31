<template>
    <div class="pie_chart_title">
        <canvas ref="pieChartCanvas" width="400" height="400"></canvas>
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
        const pieChartCanvas = ref(null);
        let pieChart;

        const createOrUpdatePieChart = () => {
            if (pieChart) {
                pieChart.destroy();
            }

            const ctx = pieChartCanvas.value;

            const datasets = {
                labels: props.data.map(coin => coin.label),
                datasets: [
                    {
                        data: props.data.map(coin => coin.data),
                        backgroundColor: props.data.map(coin => coin.backgroundColor),
                    },
                ],
            };

            pieChart = new Chart(ctx, {
                type: 'pie',
                data: datasets,
                options: {
                    responsive: false,
                    maintainAspectRatio: false,
                },
            });
        };

        onMounted(createOrUpdatePieChart);
        watch(() => props.data, createOrUpdatePieChart, { deep: true });

        return { pieChartCanvas };
    },
};
</script>
<style scoped>
.pie_chart_title h2 {
    color: #DDD9D9;
}
</style>
