<template>
    <div class="container">
        <h3>{{ image.title || "Your project" }}</h3>
        <img class="text-center" :src="getFilepath()" alt="">
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "ImageComponent",
        data() {
            return {
                image: {}
            };
        },
        async created() {
            this.image = await this.getImage();
        },
        methods: {
            getFilepath() {
                if (!this.image.filepath) {
                    return "https://i.pinimg.com/originals/10/b2/f6/10b2f6d95195994fca386842dae53bb2.png"
                }
                return "http://localhost/" + this.image.filepath
            },
            async getImage() {
                const response = await axios.get(
                    `/api/images/${this.$route.params.id}`,
                    {
                        headers: {
                            'Access-Control-Allow-Origin': '*',
                        }
                    });
                return response.data || {}
            }
        }
    }
</script>

<style scoped>

</style>