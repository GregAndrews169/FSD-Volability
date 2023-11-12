
<template class ="temp">
    <div class="info-panel">
        <h2 class="h2">Profit & Loss Analysis</h2>
        <p class="p">This is used to calculate your profit and returns from buying crypto assets from a specific time
            benchmark</p>
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

            <div class="row-column">
                <div class="column">
                    <h4 class="h4">Initial Investment</h4>
                    <span class="bottom-span">${{ initInvestment }}</span>
                </div>
                <div class="column">
                    <h4 class="h4">Profit</h4>
                    <span class="bottom-span">${{ lastProfitValue }}</span>
                </div>
                <div class="column">
                    <h4 class="h4">Return</h4>
                    <span class="bottom-span">{{ lastProfitPercent }}%</span>
                </div>
            </div>

        </div>
        <div class="chart-container">
            <LineChart :data="formattedChartData" :initialHidden="false" />
        </div><br>

        <div class="purchase-details-div">

            <div class="purchase-date-div">
                <h4 class="h4">Purchase date</h4>
                <input class="date-input2-container" type="date" v-model="purchaseDate" id="purchase-date" required />
            </div><br>


            <div class="coin-quant-div">
                <div class="coin-item">
                    <h4 class="h4">BTC</h4>
                    <input class="number-input-container" type="number" step="0.01" v-model="bitcoinQuant" id="btc-quant"
                        required />
                </div>

                <div class="coin-item">
                    <h4 class="h4">ETH</h4>
                    <input class="number-input-container" type="number" step="0.01" v-model="ethereumQuant" id="eth-quant"
                        required />
                </div>

                <div class="coin-item">
                    <h4 class="h4">TETH</h4>
                    <input class="number-input-container" type="number" step="0.01" v-model="tetherQuant" id="teth-quant"
                        required />
                </div>

                <div class="coin-item">
                    <h4 class="h4">BIN</h4>
                    <input class="number-input-container" type="number" step="0.01" v-model="binanceQuant" id="bin-quant"
                        required />
                </div>

                <div class="coin-item">
                    <h4 class="h4">XRP</h4>
                    <input class="number-input-container" type="number" step="0.01" v-model="xrpQuant" id="xrp-quant"
                        required />
                </div>

                <div class="coin-item">
                    <h4 class="h4">USDC</h4>
                    <input class="number-input-container" type="number" step="0.01" v-model="usdcQuant" id="usdc-quant"
                        required />
                </div>

                <div class="coin-item">
                    <h4 class="h4">STE</h4>
                    <input class="number-input-container" type="number" step="0.01" v-model="stellarQuant" id="ste-quant"
                        required />
                </div>

                <div class="coin-item">
                    <h4 class="h4">CAR</h4>
                    <input class="number-input-container" type="number" step="0.01" v-model="cardanoQuant" id="car-quant"
                        required />
                </div>

                <div class="coin-item">
                    <h4 class="h4">DOG</h4>
                    <input class="number-input-container" type="number" step="0.01" v-model="dogecoinQuant" id="dog-quant"
                        required />
                </div>

                <div class="coin-item">
                    <h4 class="h4">TRO</h4>
                    <input class="number-input-container" type="number" step="0.01" v-model="tronQuant" id="tro-quant"
                        required />
                </div>
            </div><br><br>

            <button class="custom-date2-button" @click.prevent="handleCustomDateSubmit2">Submit</button>

        </div>



    </div>
</template>
  
<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import LineChart from '../components/LineChart.vue';
import Sidebar from '../components/SideBar.vue';

const startDate = ref('2013-01-01');
const endDate = ref('2023-01-01');
const currentDate = ref(new Date("2021-07-06"));
const setDateRange = ref('all');
const showCustomDateInput = ref(false);
let setMetric = ref('Bitcoin');

const purchaseDate = ref('2018-01-01');
const bitcoinQuant = ref(0);
const ethereumQuant = ref(0);
const tetherQuant = ref(0);
const binanceQuant = ref(0);
const xrpQuant = ref(0);
const usdcQuant = ref(0);
const stellarQuant = ref(0);
const cardanoQuant = ref(0);
const dogecoinQuant = ref(0);
const tronQuant = ref(0);


const initInvestment = ref(0)
const lastProfitValue = ref(0)
const lastProfitPercent = ref(0)



function handleCustomDateSubmit2() {
    if (!purchaseDate.value) {
        console.error('Dates must be provided before fetching data.');
        return;
    }

    fetchData();
}

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


const lineChartData = ref([]);

const fetchData = async () => {



    try {
        const response = await axios.post('http://127.0.0.1:5000/api/profit_loss', {
            start_date: startDate.value,
            end_date: endDate.value,
            purchase_date: purchaseDate.value,
            bitcoin_quant: bitcoinQuant.value,
            ethereum_quant: ethereumQuant.value,
            tether_quant: tetherQuant.value,
            binance_quant: binanceQuant.value,
            xrp_quant: xrpQuant.value,
            usdc_quant: usdcQuant.value,
            stellar_quant: stellarQuant.value,
            cardano_quant: cardanoQuant.value,
            dogecoin_quant: dogecoinQuant.value,
            tron_quant: tronQuant.value

        });




        if (response.data) {
            const parsedData = Object.values((response.data));

            // Format data for the line chart
            const formatData = (data) => {
                return data.map(item => ({
                    x: item.Date,
                    y: item.total_portfolio
                }));
            };

            lineChartData.value = [
                {
                    label: "Total Portfolio Value",
                    data: formatData(parsedData),
                }
            ];

            initInvestment.value = parsedData[parsedData.length - 1].init_investment;

            lastProfitValue.value = parsedData[parsedData.length - 1].profit;

            lastProfitPercent.value = parsedData[parsedData.length - 1].profit_perc;



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

.date-panel {
    flex: 1;
    margin: 0 10px;
    box-sizing: border-box;
}

.date-form,
.measure-panel {
    margin: 20px 0;
}

.chart-container {
    background: linear-gradient(135deg, #2f1543 0%, #0f0e0e 100%);
    padding: 10px;
    width: 100%;
    border-radius: 10px;
}

.date-button-panel button.active,
.purchase-date-div button.active {
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
    color: #cb91f8;
    margin-bottom: 3px;
    margin-top: 10px;
}

.custom-date-button {
    background-color: #9746D6;
    color: white;
}

.purchase-details-div {
    justify-content: space-between;
    width: 100%;
    padding-top: 20px;
    padding-bottom: 20px;
    background-color: #0f0f0f;
    border-radius: 10px;
}

.coin-quant-div {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
}

.coin-item {
    flex: 0 0 calc(20% - 10px);
    margin-right: 10px;
}

.row-column {
    flex: 1;
    display: flex;
    justify-content: space-between;
    background-color: #0f0f0f;
    border-radius: 10px;
}

.column {
    flex: 1;
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
}


.number-input-container {
    height: 25px;
}

.bottom-span {
    font-weight: bold;
}
</style>
  