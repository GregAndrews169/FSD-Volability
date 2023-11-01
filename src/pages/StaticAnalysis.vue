<template>
   
    <div class="info-panel">
                <h2 class = "h2">Static Analysis</h2>
                <p class = "p">This is used to give insight into the scale and liquidity of your assets to inform asset selection decisions</p>
    </div>    

    <div class = "main">
       <div class="input-group">
            <div class="date-panel">
                <h3 class = "h3" >Date selector</h3>
                <p class = "p">Please select a date below:</p>
                
                <input type="date" class = "custom-input" v-model="startDate" id="start-date" required />
                <button class = "date-button" @click.prevent="handleCustomDateSubmit">Submit</button>
            </div>
            
            
            <div class="metric-button-panel">
                <h3 class = "h3" >Metric selector</h3>
                <p class = "p">Please select a metric below:</p>
                <button v-for="metric in metrics" :key="metric.id" @click.prevent="updateMetric(metric.id)"
                    :class="{ active: setMetric === metric.id }">
                    {{ metric.name }}
                </button>
            </div>
        </div>
        
        <div class="chart-container">
            <BarChart :data="formattedBarChartData" />
        </div>

        <div class="pie-chart-container">
            <PieChart :data="formattedBarChartData" />
        </div>


    </div>
    
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import BarChart from '../components/BarChart.vue';
import PieChart from '../components/PieChart.vue';
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
        'Cardano': '#FA5B7D',
        'Bitcoin': '#9F2DFF',
        'Ethereum': '#5089EF',
        'XRP': '#F5D232',
        'USDC': '#F69F26',
        'Tether': '#C2C3C9',
        'Stellar': '#FB7793',
        'Dogecoin': '#FFE573',
        'Tron': '#90B6FB',
        'BNB': '#FFC77A',
    };
    try {
        const response = await axios.post('http://127.0.0.1:5000/api/crypto', {
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
                },
                'XRP': {
                    label: 'XRP',
                    data: formatData(JSON.parse(response.data['coin_XRP'] || '{}')),
                    backgroundColor: colors['XRP']
                },
                'USDC': {
                    label: 'USDC',
                    data: formatData(JSON.parse(response.data['coin_USDCoin'] || '{}')),
                    backgroundColor: colors['USDC']
                },
                'Tether': {
                    label: 'Tether',
                    data: formatData(JSON.parse(response.data['coin_Tether'] || '{}')),
                    backgroundColor: colors['Tether']
                },
                'Stellar': {
                    label: 'Stellar',
                    data: formatData(JSON.parse(response.data['coin_Stellar'] || '{}')),
                    backgroundColor: colors['Stellar']
                },
                'Dogecoin': {
                    label: 'Dogecoin',
                    data: formatData(JSON.parse(response.data['coin_Dogecoin'] || '{}')),
                    backgroundColor: colors['Dogecoin']
                },
                'Tron': {
                    label: 'Tron',
                    data: formatData(JSON.parse(response.data['coin_Tron'] || '{}')),
                    backgroundColor: colors['Tron']
                },
                'BNB': {
                    label: 'BNB',
                    data: formatData(JSON.parse(response.data['coin_BinanceCoin'] || '{}')),
                    backgroundColor: colors['BNB']
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
    padding-top: 20px;
    padding-bottom: 20px;
}
.date-panel,
.metric-button-panel {
    flex: 1;
    margin: 0 10px;
    box-sizing: border-box;
    /* This ensures that padding and borders don't add to the width */
}
.metric-button-panel button.active {
    background-color: #9746D6;
    color: white;
}
.chart-container {
    background: linear-gradient(135deg, #2b3160 0%, #181616 100%);
    padding: 10px;
    margin-bottom: 20px;
}

.date-panel{
    background-color: #0f0f0f;
    border-radius: 10px;
    padding-bottom: 20px;
}

.metric-button-panel{
    background-color: #0f0f0f;
    border-radius: 10px;
}

.custom-input{
    width: 40%; /* Make the input element span the entire width */
    padding: 8px; /* Add some padding for better spacing */
    border: 1px solid #ccc; /* Add a border for better visibility */
    border-radius: 5px; /* Add rounded corners for a softer look */
    font-size: 16px; /* Adjust the font size as needed */
}

.h3{
    color: hsl(274, 92%, 75%);
    padding-bottom: 0px;
    
}

.chart-container {
    background: linear-gradient(135deg, #2f1543 0%, #0f0e0e 100%);
    padding: 10px;
    width: 100%;
    border-radius: 10px;
}

.pie-chart-container {
    background: linear-gradient(135deg, #2f1543 0%, #0f0e0e 100%);
    padding: 10px;
    width: 100%;
    border-radius: 10px;
    justify-content: center;
    align-items: center;
    display: flex;
}



.h2{
    color: hsl(274, 92%, 75%);
    padding-bottom: 0px;
    
}

.p{
    color: white;
}

.date-button{
    background-color: #9746D6;
    color: white;
    margin-left: 10px;
}



</style>