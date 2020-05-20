<template>
    <div class="container">
        <h2 class="text-center">Your Projects</h2>
        <br>
        <div class="row">
            <ImageBlock/>
        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Images",
        data() {
            return {
                images: []
            };
        },
        async created() {
            await this.getImages()
        },
        methods: {
            async getImages() {
                // this.images = await axios.post("/")
                const response = await axios.get("/api/images/");
                console.log(response.status);
                return []
            }
        }
    }
</script>

<style scoped>
    body {
        padding-top: 5rem;
    }

    .image-link:hover {
        opacity: 88%;
    }

    .image-link-text {
        color: #000;
        opacity: 76%;
    }
</style>