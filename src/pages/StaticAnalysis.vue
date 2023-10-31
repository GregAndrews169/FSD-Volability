<template>
    <div>
        <div class="input-group">
            <label>Date:</label>
            <div class="date-panel">
                <label for="start-date">Start Date:</label>
                <input type="date" v-model="startDate" id="start-date" required />

                <button @click.prevent="handleCustomDateSubmit">Submit</button>


            </div>
            <label for="metric">Metric:</label>
            <div class="metric-button-panel">
                <button v-for="metric in metrics" :key="metric.id" @click.prevent="updateMetric(metric.id)"
                    :class="{ active: setMetric === metric.id }">
                    {{ metric.name }}
                </button>
            </div>
        </div>

        <div class="chart-container">
            <BarChart :data="formattedBarChartData" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import BarChart from '../components/BarChart.vue';

const setMetric = ref('volume');
const barChartData = ref([]);

const startDate = ref('2020-01-03');  // replace with your desired start date
const endDate = ref('2020-01-04');

const metrics = [
    { id: 'volume', name: 'Volume' },
    { id: 'market-cap', name: 'Market Cap' }
];

const updateMetric = (metricId) => {
    setMetric.value = metricId;
    fetchData(); // Optionally re-fetch data after updating the metric
};

function handleCustomDateSubmit() {
    if (!startDate.value) {
        console.error('Dates must be provided before fetching data.');
        return;
    }

    // Compute end date based on start date
    let end = new Date(startDate.value);
    end.setDate(end.getDate() + 1);
    endDate.value = end.toISOString().split('T')[0]; // Convert the date object back to the YYYY-MM-DD format

    fetchData();
}

const fetchData = async () => {
    const metricMap = {
        'volatility': 'Volatility',
        'open': 'Open',
        'close': 'Close',
        'volume': 'Volume',
        'market-cap': 'Marketcap'
    };

    const colors = {
        'Cardano': 'red',
        'Bitcoin': 'blue',
        'Ethereum': 'yellow'
    };

    try {
        const response = await axios.post('http://localhost:5000/api/crypto', {

            start_date: startDate.value,
            end_date: endDate.value
        });

        if (response.data) {
            const formatData = (data) => {
                const metricValue = metricMap[setMetric.value];
                // Since it's a bar chart with a single row of data, take the first data object
                const firstDataObj = Object.values(data)[0];
                return firstDataObj ? [firstDataObj[metricValue]] : [null];
            };

            barChartData.value = {
                'Cardano': {
                    label: 'Cardano',
                    data: formatData(JSON.parse(response.data['coin_Cardano'] || '{}')),
                    backgroundColor: colors['Cardano']
                },
                'Bitcoin': {
                    label: 'Bitcoin',
                    data: formatData(JSON.parse(response.data['coin_Bitcoin'] || '{}')),
                    backgroundColor: colors['Bitcoin']
                },
                'Ethereum': {
                    label: 'Ethereum',
                    data: formatData(JSON.parse(response.data['coin_Ethereum'] || '{}')),
                    backgroundColor: colors['Ethereum']
                }
            };
        } else {
            console.error('No data received');
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

onMounted(fetchData);

const formattedBarChartData = computed(() => {
    return Object.values(barChartData.value);
});


</script>

<style scoped>
.input-group {
    display: flex;
    justify-content: space-between;
    width: 100%;
    flex-wrap: wrap;
}

.date-panel,
.metric-button-panel {
    flex: 1;
    margin: 0 10px;
    box-sizing: border-box;
    /* This ensures that padding and borders don't add to the width */
}

.metric-button-panel button.active {
    background-color: #4caf50;
    color: white;
}

.chart-container {
    background: linear-gradient(135deg, #2b3160 0%, #181616 100%);
    padding: 10px;
}
</style>
