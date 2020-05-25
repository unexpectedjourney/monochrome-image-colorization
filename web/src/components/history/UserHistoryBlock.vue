<template>
    <div class="container">
        <p>{{getRecordString()}}</p>
        <hr>
    </div>
</template>

<script>
    import {localization} from "../../localization/localization";

    export default {
        name: "UserHistoryBlock",
        props: ["record"],
        methods: {
            getRecordString() {
                const type = this.record.type
                if (type === 1) {
                    return `${this.getLang.you} ${this.getLang.colorizedFile} ${this.record.created_at}`
                } else if (type === 2) {
                    return `${this.getLang.you} ${this.getLang.savedFile} ${this.record.created_at}`
                } else if (type === 3) {
                    return `${this.getLang.you} ${this.getLang.loggedIn} ${this.record.created_at}`
                } else if (type === 4) {
                    return `${this.getLang.you} ${this.getLang.signedUp} ${this.record.created_at}`
                } else if (type === 5) {
                    return `${this.getLang.you} ${this.getLang.updatedProfile} ${this.record.created_at}`
                } else if (type === 6) {
                    return `${this.getLang.you} ${this.getLang.addedNote} ${this.record.created_at}`
                } else if (type === 7) {
                    return `${this.getLang.you} ${this.getLang.deletedNote} ${this.record.created_at}`
                }
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