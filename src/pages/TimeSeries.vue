
<template class ="temp">
    <div class="info-panel">
        <h2 class="h2">Time Series Analysis</h2>
        <p class="p">This is used to understand the behaviour of your assets over a period of time to inform buy, sell or
            hold descisions.</p>
    </div>

    <div class="main">
        <div class="date-and-measure-container">
            <div class="date-panel">
                <h3 class="h3">Date selector</h3>
                <p class="p">Please select your date below:</p>
                <form class="date-form">

                    <div class="date-button-panel">
                        <button @click.prevent="updateDateRange('week')" :class="{ active: setDateRange === 'week' }">
                            Week
                        </button>

                        <button @click.prevent="updateDateRange('month')" :class="{ active: setDateRange === 'month' }">
                            Month
                        </button>

                        <button @click.prevent="updateDateRange('year')" :class="{ active: setDateRange === 'year' }">
                            Year
                        </button>

                        <button @click.prevent="updateDateRange('all')" :class="{ active: setDateRange === 'all' }">
                            All
                        </button>

                        <button @click.prevent="toggleCustomDateInput" :class="{ active: setDateRange === 'custom' }">
                            Custom
                        </button>
                    </div>

                    <div class="custom-date-div" v-if="showCustomDateInput">
                        <div class="start-date-div">
                            <h4 class="h4">Start date</h4>
                            <input class="date-input-container" type="date" v-model="startDate" id="start-date" required />
                        </div>

                        <div class="end-date-div">
                            <h4 class="h4">End date</h4>
                            <input class="date-input-container" type="date" v-model="endDate" id="end-date" required />
                        </div>

                        <button class="custom-date-button" @click.prevent="handleCustomDateSubmit">Submit</button>

                    </div>
                </form>

            </div>

            <div class="measure-panel">
                <h3 class="h3">Metric selector</h3>
                <p class="p">Please select your metric below:</p>
                <form class="measure-form">

                    <div class="measure-button-panel">
                        <button @click.prevent="updateMetric('volatility')" :class="{ active: setMetric === 'volatility' }">
                            Volatility
                        </button>

                        <button @click.prevent="updateMetric('close')" :class="{ active: setMetric === 'close' }">
                            Price
                        </button>

                        <button @click.prevent="updateMetric('volume')" :class="{ active: setMetric === 'volume' }">
                            Volume
                        </button>

                        <button @click.prevent="updateMetric('market-cap')" :class="{ active: setMetric === 'market-cap' }">
                            Market Cap
                        </button>
                    </div>
                </form>

            </div>
        </div>

        <div class="info-panel">
            <h4 class="h2">Time Series Line Chart</h4>
            <p class="p2">Please select an asset in the legend below to add the Line Chart:</p>
        </div>

        <div class="chart-container">
            <LineChart :data="formattedChartData" :initialHidden="true" />
        </div>

    </div>
</template>
  
<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import LineChart from '../components/LineChart.vue';
import Sidebar from '../components/SideBar.vue';

const startDate = ref('2016-01-01');
const endDate = ref('2023-01-01');
const currentDate = ref(new Date("2021-07-06"));
const setDateRange = ref('all');
let setMetric = ref('volatility');
const showCustomDateInput = ref(false);

function handleCustomDateSubmit() {
    if (!startDate.value || !endDate.value) {
        console.error('Dates must be provided before fetching data.');
        return;
    }
    fetchData();
}

watch(setDateRange, (newValue) => {
    const tempDate = new Date(currentDate.value);
    switch (newValue) {
        case 'week':
            startDate.value = formatDate(new Date(tempDate.setDate(tempDate.getDate() - 7)));
            endDate.value = formatDate(currentDate.value);
            break;
        case 'month':
            startDate.value = formatDate(new Date(tempDate.setMonth(tempDate.getMonth() - 1)));
            endDate.value = formatDate(currentDate.value);
            break;
        case 'year':
            startDate.value = formatDate(new Date(tempDate.setFullYear(tempDate.getFullYear() - 1)));
            endDate.value = formatDate(currentDate.value);
            break;
        case 'all':
            startDate.value = "2013-01-01";
            endDate.value = "2023-01-01";
            break;
    }
    fetchData();
});


function toggleCustomDateInput() {
    showCustomDateInput.value = !showCustomDateInput.value;
    if (showCustomDateInput.value) {
        setDateRange.value = 'custom';
    }
}

function updateDateRange(range) {
    setDateRange.value = range;
    if (range !== 'custom') {
        showCustomDateInput.value = false;
    }
}

function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function updateMetric(range) {
    setMetric.value = range;
    fetchData();
}

const lineChartData = ref([]);

const fetchData = async () => {

    const metricMap = {
        'volatility': 'Volatility',
        'open': 'Open',
        'close': 'Close',
        'volume': 'Volume',
        'market-cap': 'Marketcap'
    };

    try {
        const response = await axios.post('http://127.0.0.1:5000/api/crypto', {
            start_date: startDate.value,
            end_date: endDate.value,
        });

        if (response.data) {
            const formatData = (data) => {
                const metricValue = metricMap[setMetric.value];
                return Object.values(data).map(item => ({
                    x: item.Date,
                    y: item[metricValue]
                }));
            };

            lineChartData.value = [
                {
                    label: 'Cardano',
                    data: formatData(JSON.parse(response.data['coin_Cardano'] || '{}')),
                },
                {
                    label: 'Bitcoin',
                    data: formatData(JSON.parse(response.data['coin_Bitcoin'] || '{}')),
                },
                {
                    label: 'Ethereum',
                    data: formatData(JSON.parse(response.data['coin_Ethereum'] || '{}')),
                },
                {
                    label: 'XRP',
                    data: formatData(JSON.parse(response.data['coin_XRP'] || '{}')),
                },
                {
                    label: 'USDC',
                    data: formatData(JSON.parse(response.data['coin_USDCoin'] || '{}')),
                },
                {
                    label: 'Tether',
                    data: formatData(JSON.parse(response.data['coin_Tether'] || '{}')),
                },
                {
                    label: 'Stellar',
                    data: formatData(JSON.parse(response.data['coin_Stellar'] || '{}')),
                },
                {
                    label: 'Dogecoin',
                    data: formatData(JSON.parse(response.data['coin_Dogecoin'] || '{}')),
                },
                {
                    label: 'Tron',
                    data: formatData(JSON.parse(response.data['coin_Tron'] || '{}')),
                },
                {
                    label: 'BNB',
                    data: formatData(JSON.parse(response.data['coin_BinanceCoin'] || '{}')),
                }

            ];
        } else {
            console.error('No data received');
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

onMounted(fetchData);

const formattedChartData = computed(() => lineChartData.value);
</script>
<style scoped>
.date-and-measure-container {
    display: flex;
    justify-content: space-between;
    width: 100%;
    flex-wrap: wrap;
    padding-top: 20px;
    padding-bottom: 20px;
}

.date-panel,
.measure-panel {
    flex: 1;
    margin: 0 10px;
    box-sizing: border-box;
}

.date-form,
.measure-form {
    margin: 20px 0;
}

.chart-container {
    background: linear-gradient(135deg, #2f1543 0%, #0f0e0e 100%);
    padding: 10px;
    width: 100%;
    border-radius: 10px;
}

.date-button-panel button.active,
.measure-button-panel button.active {
    background-color: #9746D6;
    color: white;
}

.p {
    color: white;
}

.h3 {
    color: hsl(274, 92%, 75%);
    padding-bottom: 0px;

}

.h2 {
    color: hsl(274, 92%, 75%);
    padding-bottom: 0px;

}

.date-panel {
    background-color: #0f0f0f;
    border-radius: 10px;
}

.measure-panel {
    background-color: #0f0f0f;
    border-radius: 10px;
}

.temp {
    border-radius: 10px;
}

.custom-date-div {
    padding-top: 10px;
    padding-bottom: 20px;
}

.custom-date-div {
    background-color: #000000;
    max-width: 200px;
    margin-left: 240px;
    margin-top: 20px;
    border-radius: 10px;
}

.start-date-div {
    padding-bottom: 10px;
}

.end-date-div {
    padding-bottom: 20px;
}

.date-input-container {
    padding: 8px;
}

.h4 {
    color: rgb(203, 145, 248);
    margin-bottom: 3px;
    margin-top: 10px;
}

.custom-date-button {
    background-color: #9746D6;
    color: white;
}
</style>
  