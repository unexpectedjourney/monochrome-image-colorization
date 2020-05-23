<template>
    <div class="media">
        <div class="media-body">
            <h4 class="media-heading">Your note</h4>
            <p>{{note.text}}</p>
            <ul class="list-unstyled list-inline media-detail pull-left">
                <li class=""><i class="fa fa-calendar"></i> {{getDate()}}</li>
                <li class=""><button v-on:click="removeNote(note._id)" type="button" class="btn btn-outline-danger"><i class="fa fa-trash"></i> Remove</button></li>
            </ul>
            <hr/>
        </div>
    </div>
</template>

<script>
    export default {
        name: "NoteBlock",
        props: ["note", "removeNote"],
        methods: {
            getDate() {
                if (this.created_at) {
                    return this.created_at.split("T")[0];
                }
                return new Date().toISOString().split("T")[0]
            }
        }
    }
</script>

<style scoped>

</style>