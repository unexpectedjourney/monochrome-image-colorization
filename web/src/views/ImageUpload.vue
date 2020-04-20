<template>
    <div class="container">
        <div class="large-12 medium-12 small-12 cell">
            <label>File
                <input type="file" id="file" ref="file"
                       v-on:change="handleFileUpload()"/>
            </label>
            <button v-on:click="submitFile()">Submit</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8080/api'

export default {
    name: "ImageUpload",
    data() {
        return {
            file: ''
        }
    },
    methods: {
        async submitFile() {
            let formData = new FormData();
            formData.append('file', this.file);

            let result = await axios.post('/colorize_file',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            )
            console.log(result);
        },
        handleFileUpload() {
            this.file = this.$refs.file.files[0];
        }
    }
}
</script>

<style scoped>

</style>