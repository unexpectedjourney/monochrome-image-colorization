<template>
    <div class="media">
        <div class="media-body">
            <h4 class="media-heading">{{getLang.yourNote}}</h4>
            <p>{{note.text}}</p>
            <ul class="list-unstyled list-inline media-detail pull-left">
                <li class=""><i class="fa fa-calendar"></i> {{getDateWrapper()}}</li>
                <li class=""><button v-on:click="removeNote(note._id)" type="button" class="btn btn-outline-danger"><i class="fa fa-trash"></i>
                    {{getLang.remove}}</button></li>
            </ul>
            <hr/>
        </div>
    </div>
</template>

<script>
    import date from "../helpers/date";
    import {localization} from "../localization/localization";

    export default {
        name: "NoteBlock",
        props: ["note", "removeNote"],
        computed: {
            getLang() {
                if (this.$store.getters.getLocalization) {
                    return localization.en;
                }
                return localization.ua;
            },
        },
        methods: {
            getDateWrapper() {
                return date.getDate(this.note.created_at)
            },
        }
    }
</script>

<style scoped>

</style>