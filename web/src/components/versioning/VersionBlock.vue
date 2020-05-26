<template>
    <div>
        <h3>{{getLang.version}} #{{versionIndex}}</h3>
        <img class="rounded img-fluid"
             :src="getFilepathWrapper()"
             width="300" height="300">
        <ul class="list-unstyled list-inline media-detail pull-left">
            <li class="list-inline-item"><i class="fa fa-calendar"></i>
                {{getDateWrapper()}}
            </li>
            <li class="list-inline-item"><a type="button"
                                            :href="getFilepathWrapper()"
                                            class="btn btn-outline-success"><i
                    class="fa fa-download"></i>{{getLang.download}}</a></li>
        </ul>
        <hr>
    </div>
</template>

<script>
    import filepath from '../../helpers/filepath';
    import date from '../../helpers/date';
    import {localization} from "../../localization/localization";

    export default {
        name: "VersionBlock",
        props: ["version", "versionIndex"],
        computed: {
            getLang() {
                if (this.$store.getters.getLocalization) {
                    return localization.en;
                }
                return localization.ua;
            },
        },
        methods: {
            getFilepathWrapper() {
                return filepath.getFilepath(this.version.filepath)
            },
            getDateWrapper() {
                return date.getDate(this.version.created_at)
            }
        }
    }
</script>

<style scoped>

</style>