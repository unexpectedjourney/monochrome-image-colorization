<template>
    <div class="container">
        <h2 class="text-center">{{getLang.yourProjects}}</h2>
        <br>
        <div v-if="images.length != 0" class="row">
            <ImageBlock v-for="image in images" v-bind:key="image._id" v-bind:image="image" />
        </div>
        <div v-else>
            <p>{{getLang.noData}}</p>
        </div>
    </div>
</template>

<script>
    import axios from "axios";
    import ImageBlock from "./ImageBlock"
    import {localization} from "../localization/localization";

    export default {
        name: "Images",
        components: {
            ImageBlock
        },
        data() {
            return {
                images: []
            };
        },
        async created() {
            this.images = await this.getImages();
        },
        computed: {
            getLang() {
                if (this.$store.getters.getLocalization) {
                    return localization.en;
                }
                return localization.ua;
            },
        },
        methods: {
            async getImages() {
                const response = await axios.get("/api/images/");
                return response.data || [];
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