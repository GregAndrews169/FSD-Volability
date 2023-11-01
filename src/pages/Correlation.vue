<template>
    
    <div>
        <h2 class = "h2">Correlation Analysis</h2>
        <p class = "p">This is used to understand the correlation between certain assets in your portfolio to inform your asset selection process</p>
    </div>   
    
    <div class="main">
        <div class="date-and-measure-container">
            <!-- Date Panel from TimeSeries.vue -->
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

                    <div class = "custom-date-div" v-if="showCustomDateInput">
                        <div class="start-date-div">
                        <h4 class = "h4">Start date</h4>
                        <input class = "date-input-container" type="date" v-model="startDate" id="start-date" required />
                        </div>

                        <div class="end-date-div">
                        <h4 class = "h4">End date</h4>
                        <input class = "date-input-container" type="date" v-model="endDate" id="end-date" required />
                        </div>

                        <button class = "custom-date-button" @click.prevent="handleCustomDateSubmit">Submit</button>

                    </div>
                </form>
            </div>

            <!-- If you need a Metric Panel you can add it here -->

        </div>

        <div class="chart-container">
            <Heatmap :matrix-data="correlationMatrix" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import Heatmap from '../components/HeatMap.vue';

// Variables from TimeSeries.vue
const setDateRange = ref('all');
const showCustomDateInput = ref(false);

const startDate = ref('2018-01-01');
const endDate = ref('2019-12-31');

const currentDate = ref(new Date("2021-07-06"));

function handleCustomDateSubmit() {
    if (!startDate.value || !endDate.value) {
        console.error('Dates must be provided before fetching data.');
        return;
    }
    fetchData();
}

// Methods from TimeSeries.vue
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

const correlationMatrix = ref([]);

const fetchData = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:5000/api/correlation', {
            start_date: startDate.value,
            end_date: endDate.value,
        });
        correlationMatrix.value = response.data;
        console.log("Data fetched from API:", correlationMatrix.value);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};


onMounted(fetchData);
</script>

<style scoped>
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
  flex: 1;
  margin: 10px;
  box-sizing: border-box;
  background-color: #0f0f0f;
  border-radius: 10px;
  max-width: 500px;
  padding-bottom: 20px;
}

.date-button-panel button.active {
  background-color: #9746D6;
  color: white;
}

.date-and-measure-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
  flex-wrap: wrap;
  padding-top: 20px;
  padding-bottom: 20px;
  padding-left: 220px;
  align-items: center;
}

.custom-date-div{
    padding-top: 10px;
    padding-bottom: 20px;
}

.custom-date-div{
    background-color: #000000;
    max-width: 200px;
    margin-left: 240px;
    margin-top: 20px;
    border-radius: 10px;
}

.start-date-div{
    padding-bottom: 10px;
}

.end-date-div{
    padding-bottom: 20px;
}

.date-input-container{
    padding: 8px;
}

.h4{
    color: #cb91f8;
    margin-bottom: 3px;
    margin-top: 10px;
}

.custom-date-button {
    background-color: #9746D6;
    color: white;
}

</style>
