<template>
    <div>
        <h3>Version #{{versionIndex}}</h3>
        <img class="rounded img-fluid"
                 :src="getFilepathWrapper()"
                 width="300" height="300">
        <ul class="list-unstyled list-inline media-detail pull-left">
            <li class="list-inline-item"><i class="fa fa-calendar"></i> {{getDateWrapper()}}</li>
            <li class="list-inline-item"><a type="button" :href="getFilepathWrapper()" class="btn btn-outline-success"><i class="fa fa-download"></i> Download</a></li>
        </ul>
        <hr>
    </div>
</template>

<script>
    import filepath from '../../helpers/filepath';
    import date from '../../helpers/date';
    export default {
        name: "VersionBlock",
        props: ["version", "versionIndex"],
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