<template>
    <div class="container">
        <h2>{{getLang.yourHistory}}</h2>
        <div v-if="history.length !== 0">
            <UserHistoryBlock v-for="(record, index) in history"
                              v-bind:key="record._id" v-bind:record="record"/>
        </div>
        <div v-else>
            <p>{{getLang.noData}}</p>
        </div>

    </div>
</template>

<script>
    import UserHistoryBlock from "./UserHistoryBlock";
    import axios from "axios";
    import {localization} from "../../localization/localization";

    export default {
        name: "UserHistory",
        components: {
            UserHistoryBlock
        },
        data() {
            return {
                history: []
            }
        },
        async created() {
            this.history = await this.getUserHistory();
        },
        methods: {
            async getUserHistory() {
                const response = await axios.get(
                    `/api/history/`,
                    {
                        headers: {
                            'Access-Control-Allow-Origin': '*',
                        }
                    }
                );
                return response.data || [];
            }
        },
        computed: {
            getLang() {
                if (this.$store.getters.getLocalization) {
                    return localization.en;
                }
                return localization.ua;
            },
        },
    }
</script>

<style scoped>

</style>