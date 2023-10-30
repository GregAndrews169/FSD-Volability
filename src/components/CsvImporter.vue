<template>
    <div>
        <input type="file" accept=".csv" @change="handleFileUpload($event)" />
    </div>
</template>
  
<script>
import Papa from 'papaparse';

export default {
    data() {
        return {
            file: '',
            content: [],
            parsed: false
        }
    },

    methods: {
        handleFileUpload(event) {
            this.file = event.target.files[0];
            this.processCSVFile(this.file); // Passing the file here
        },


        processCSVFile() {
            Papa.parse(this.file, {
                header: true, // Assuming the first row contains headers
                dynamicTyping: true, // Automatically convert numeric values
                skipEmptyLines: true, // Skip rows with empty values
                complete: (results) => {
                    this.content = results;
                    this.parsed = true;
                    results.data.forEach((row) => {
                        delete row['normalized-losses'];
                    });
                    //clean data by removing ?
                    const filteredData = results.data.filter(row => !Object.values(row).includes('?'));

                    this.$emit('csv-data-loaded', results.data); // Emitting data to the parent
                },
            });
        },
    },
};
</script>
