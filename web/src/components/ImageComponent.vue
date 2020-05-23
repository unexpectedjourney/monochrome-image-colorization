<template>
    <div class="container">
        <h3>{{ image.title || "Your project" }}</h3>
        <img class="text-center" :src="getFilepath()" alt="">
        <div class="row">
            <div class="col-sm-12">
                <form class="form-group">
                    <h3 class="pull-left">New Comment</h3>
                    <fieldset>
                        <div class="row">
                            <div class="form-group col-xs-12 col-sm-12 col-lg-12">
                                <textarea class="form-control" id="message"
                                          placeholder="Your message"
                                          required=""
                                          v-model="commentText"></textarea>
                            </div>
                        </div>
                    </fieldset>
                    <button v-on:click="addNote($event)"
                            class="btn btn-primary sumbit-button">
                        Submit
                    </button>
                </form>
                <h3>{{ getCommentsNumber() }} Notes</h3>
                <hr/>
                <NoteBlock v-for="note in image.notes" v-bind:key="note._id"
                           v-bind:note="note" v-bind:remove-note="removeNote"/>

            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios";
    import NoteBlock from "./NoteBlock";

    export default {
        name: "ImageComponent",
        components: {NoteBlock},
        data() {
            return {
                image: {
                    notes: []
                },
                commentText: null
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
            },
            getCommentsNumber() {
                return this.image.notes.length
            },
            async addNote(event) {
                if (event) {
                    event.preventDefault()
                }
                let data = {
                    "text": this.commentText,
                    "file_id": this.image._id
                }
                this.image.notes.unshift({"text": this.commentText})
                this.commentText = ""
                const response = await axios.post("/api/note/", data)
                this.image = await this.getImage();
            },
            async removeNote(id) {
                this.image.notes = this.image.notes.filter(
                    note => note._id !== id
                );
                const response = await axios.delete(`/api/note/${id}`)
            }
        }
    }
</script>

<style scoped>
    .sumbit-button {
        margin-bottom: 13px;
        /*float: right*/
    }
</style>