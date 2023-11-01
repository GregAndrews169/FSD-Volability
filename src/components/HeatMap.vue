<template>
    <div class="chart-container">
        <canvas ref="matrixChart" width="950" height="800"></canvas>
    </div>
</template>

<script>
import { ref, watchEffect } from 'vue';
import 'https://cdn.jsdelivr.net/npm/chart.js@3.7';
import 'https://cdn.jsdelivr.net/npm/chartjs-chart-matrix@1.1';

export default {
    name: 'Heatmap',
    props: {
        matrixData: {
            type: Array,
            required: true
        },
        labels: {
            type: Array,
            default: () => [
                "Bitcoin",
                "Ethereum",
                "Tether",
                "Binance Coin",
                "XRP",
                "USD Coin",
                "Stellar",
                "Cardano",
                "Dogecoin",
                "Tron"
            ]

        },

        labels2: {
            type: Array,
            default: () => [
                "Tron",
                "Dogecoin",
                "Cardano",
                "Stellar",
                "USD Coin",
                "XRP",
                "Binance Coin",
                "Tether",
                "Ethereum",
                "Bitcoin"
            ]


        }
    },
    setup(props) {
        const matrixChart = ref(null);
        const matrixChartInstance = ref(null);

        console.log("Matrix Data Prop in Heatmap:", props.matrixData);  // Logging data when component sets up

        const initChart = () => {
            const n = Math.sqrt(props.matrixData.length); // Determine the dimension 'n' based on the length of matrixData
            if (matrixChartInstance.value) {
                matrixChartInstance.value.destroy(); // destroy the previous instance
            }
            matrixChartInstance.value = new Chart(matrixChart.value.getContext('2d'), {
                type: 'matrix',
                data: {
                    datasets: [{
                        labels: props.labels,
                        data: props.matrixData,
                        borderWidth: 1,
                        backgroundColor({ raw }) {
                            const alpha = raw.v;  // Assuming raw.v is between 0 and 1
                            const baseColor = `255, 255, 255`;  // RGB for purple color
                            return `rgba(${baseColor}, ${alpha})`;
                        },
                        borderColor: 'rgb(236, 228, 228, 0.7)',
                        width: ({ chart }) => (chart.chartArea || {}).width / n - 1,
                        height: ({ chart }) => (chart.chartArea || {}).height / n - 1,
                    }],
                },
                options: {
                    scales: {
                        x: {
                            display: true,
                            min: 1,
                            max: n + 1,
                            offset: false,
                            beginAtZero: true,
                            ticks: {
                                padding: 40,
                                callback: function (value, index, ticks) {
                                    // Check if the index is within bounds
                                    if (index < props.labels.length) {
                                        return props.labels[index];
                                    }
                                }
                            }
                        },
                        y: {
                            display: true,
                            min: 0,
                            max: n,
                            beginAtZero: true,
                            reverse: true,
                            ticks: {
                                padding: 40,
                                callback: function (value, index, ticks) {
                                    if (index < props.labels2.length) {
                                        return props.labels2[index];
                                    }
                                }
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            enabled: true,
                            callbacks: {
                                label: function (context) {
                                    const value = context.raw.v;
                                    const roundedValue = Math.round(value * 100 / 1);
                                    return 'Value: ' + roundedValue;
                                }
                            }
                        }
                    },
                    legend: {
                        display: false
                    }
                }
            });
        }

        watchEffect(() => {
            if (props.matrixData && props.matrixData.length) {
                initChart();
            }
        });

        return {
            matrixChart
        }
    }
}
</script>

<style scoped>
/* Optional styles */
</style>
