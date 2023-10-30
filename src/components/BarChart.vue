<template>
    <div>
        <h2>Bar Chart</h2>
        <canvas ref="barChartCanvas" width="400" height="200"></canvas>
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
        let chart = null;

        // Create the bar chart
        const createBarChart = () => {
            if (chart) {
                chart.destroy(); // Destroy the existing chart if it exists
            }

            const dataArray = props.data.map(d => ({ x: d.make, y: d.price }))
            const makes = Array.from(new Set(dataArray.map(d => d.x)))

            const makeMeanPrices = {};

            makes.forEach(m => {
                const makePrice = dataArray.
                    filter(s => s.x === m).
                    map(d => d.y);

                const sumPrice = makePrice.reduce((total, num) => total + num, 0);
                const makeLength = makePrice.length

                makeMeanPrices[m] = sumPrice / makeLength;
            })

            console.log(makeMeanPrices);

            var makeMeanPricesSorted = Object.keys(makeMeanPrices).map(function (key) {
                return [key, makeMeanPrices[key]];
            });

            // Sort the array based on the second element
            makeMeanPricesSorted.sort(function (first, second) {
                return first[1] - second[1];
            });

            // Extract sorted makes and averagePrices from the sorted array
            const labels = makeMeanPricesSorted.map(d => d[0]);
            const prices = makeMeanPricesSorted.map(d => d[1]);

            const ctx = barChartCanvas.value.getContext('2d');
            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Average Price',
                            data: prices,
                            backgroundColor: 'rgba(200, 100, 200, 0.2)',
                            borderColor: 'rgba(200, 100, 200, 1)',
                            borderWidth: 1,
                        },
                    ],
                },
                options: {
                    scales: {
                        y: {
                            type: 'linear',
                            position: 'top',
                            beginAtZero: true,
                        },
                    },
                },
            });
        };

        onMounted(() => {
            createBarChart();
        });

        watch(() => props.data, () => {
            // Re-render the bar chart when data changes
            createBarChart();
        });

        return {
            barChartCanvas,
        };
    },
};
</script>

