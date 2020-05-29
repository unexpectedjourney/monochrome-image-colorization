<template>
    <div class="container">
        <h3>{{ image.title || getLang.yourProject }}</h3>
        <img class="text-center" :src="getFilepathWrapper()" alt="">
        <ul class="list-unstyled list-inline media-detail pull-left">
            <li class="list-inline-item">
                <router-link :to="{name: 'versions'}" type="button"
                             class="btn btn-outline-info"><i
                        class="fa fa-clone"></i> {{getLang.imageVersions}}
                </router-link>
            </li>
            <li class="list-inline-item">
                <router-link
                        :to="{name: 'image_editor', params: {file_id: image._id}}"
                        type="button"
                        class="btn btn-outline-success"><i
                        class="fa fa-download"></i> {{getLang.edit}}
                </router-link>
            </li>
            <li class="list-inline-item"><a type="button"
                                            :href="getFilepathWrapper()"
                                            class="btn btn-outline-success"><i
                    class="fa fa-download"></i> {{getLang.download}}</a></li>
        </ul>
        <div class="row">
            <div class="col-sm-12">
                <form class="form-group">
                    <h3 class="pull-left">{{getLang.newNote}}</h3>
                    <fieldset>
                        <div class="row">
                            <div class="form-group col-xs-12 col-sm-12 col-lg-12">
                                <textarea class="form-control" id="message"
                                          :placeholder="[[ getLang.yourMessage ]]"
                                          required=""
                                          v-model="commentText"></textarea>
                            </div>
                        </div>
                    </fieldset>
                    <button v-on:click="addNote($event)"
                            class="btn btn-primary sumbit-button">
                        {{getLang.submit}}
                    </button>
                </form>
                <h3>{{ getCommentsNumber() }} {{getLang.notes}}</h3>
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
    import filepath from "../helpers/filepath";
    import {localization} from "../localization/localization";

    export default {
        name: "ImageInfo",
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
                return filepath.getFilepath(this.image.filepath);
            },
            async getImage() {
                const response = await axios.get(
                    `/api/images/${this.$route.params.id}/`,
                    {
                        headers: {
                            'Access-Control-Allow-Origin': '*',
                        }
                    });
                return response.data || {};
            },
            getCommentsNumber() {
                return this.image.notes.length;
            },
            async addNote(event) {
                if (event) {
                    event.preventDefault();
                }
                let data = {
                    "text": this.commentText,
                    "file_id": this.image._id
                }
                this.image.notes.unshift({"text": this.commentText});
                this.commentText = "";
                const response = await axios.post("/api/note/", data);
                this.image = await this.getImage();
            },
            async removeNote(id) {
                this.image.notes = this.image.notes.filter(
                    note => note._id !== id
                );
                const response = await axios.delete(`/api/note/${id}/`);
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