<template>
    <div class="main">
        <div class="date-and-measure-container">
            <!-- Date Panel from TimeSeries.vue -->
            <div class="date-panel">
                <h3 class="h3">Date Selector</h3>
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

                    <div v-if="showCustomDateInput">
                        <label for="start-date">Start Date:</label>
                        <input type="date" v-model="startDate" id="start-date" required />

                        <label for="end-date">End Date:</label>
                        <input type="date" v-model="endDate" id="end-date" required />

                        <button @click.prevent="handleCustomDateSubmit">Submit</button>

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
/* Merged styles from TimeSeries.vue */
/* ... (add styles from TimeSeries.vue and modify if needed) */
</style>
