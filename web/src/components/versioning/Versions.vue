<template>
    <div class="container">
        <VersionBlock v-for="(version, index) in image.versions"
                      v-bind:key="version._id" v-bind:version="version"
                      v-bind:version-index="getVersionIndex(index)"/>
    </div>
</template>

<script>
    import VersionBlock from "./VersionBlock";
    import axios from "axios";

    export default {
        name: "Versions",
        components: {
            VersionBlock
        },
        data() {
            return {
                "image": {}
            }
        },
        async created() {
            this.image = await this.getImageVersions();
        },
        methods: {
            async getImageVersions() {
                const response = await axios.get(
                    `/api/images/${this.$route.params.id}/versions/`,
                    {
                        headers: {
                            'Access-Control-Allow-Origin': '*',
                        }
                    });
                return response.data || {};
            },
            getVersionIndex(index) {
                return this.image.versions.length - index;
            }
        }
    }
</script>

<style scoped>

</style>