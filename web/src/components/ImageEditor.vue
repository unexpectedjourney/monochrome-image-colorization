<template>
    <div>
        <div id="app" class="main">
            <div class="editor-container">
                <div class="row">
                    <div class="form-group text-centered mx-auto col-md-12">
                        <label for="projectTitleData">{{getLang.projectTitle}}</label>
                        <input type="text" class="form-control"
                               id="projectTitleData"
                               :placeholder="[[ getLang.projectTitle ]]"
                               v-model="projectTitle">
                    </div>
                </div>
                <div class="editor">
                    <div class="current-color"
                         :style="{ backgroundColor: color }"></div>

                    <Tool :event="() => undo()"
                          :iconClass="'fas fa-undo-alt fa-lg'"/>

                    <Tool :event="() => redo()"
                          :iconClass="'fas fa-redo-alt fa-lg'"/>

                    <Tool :event="() => clear()"
                          :iconClass="'fas fa-trash-alt fa-lg'"/>

                    <Tool
                            :event="() => setTool('freeDrawing')"
                            :iconClass="'fas fa-pencil-alt fa-lg'"
                            :class="{ 'active-tool': currentActiveMethod === 'freeDrawing' }"
                    />

                    <Tool
                            :event="() => setTool('circle')"
                            :iconClass="'far fa-circle fa-lg'"
                            :class="{ 'active-tool': currentActiveMethod === 'circle' }"
                    />

                    <Tool
                            :event="() => setTool('rect')"
                            :iconClass="'far fa-square fa-lg'"
                            :class="{ 'active-tool': currentActiveMethod === 'rect' }"
                    />

                    <Tool
                            :event="() => setTool('arrow')"
                            :iconClass="'fas fa-long-arrow-alt-down fa-lg'"
                            :class="{ 'active-tool': currentActiveMethod === 'arrow' }"
                    />

                    <Tool
                            :event="() => setTool('selectMode')"
                            :iconClass="'fas fa-arrows-alt fa-lg'"
                            :class="{ 'active-tool': currentActiveMethod === 'selectMode' }"
                    />

                    <Tool
                            :event="() => applyCropping()"
                            :iconClass="'far fa-check-circle fa-lg'"
                            v-show="croppedImage"
                            :class="{ 'active-tool': currentActiveMethod === 'crop' }"
                    />

                    <Tool
                            :event="e => uploadImage(e)"
                            :iconClass="'fas fa-file-upload fa-lg'"
                            :labelForUploadImage="true"
                    />
                    <Tool :event="() => saveImage()"
                          :iconClass="'fas fa-download fa-lg'"/>
                    <Tool v-if="!imageUrl"
                          :key="imageUrl"
                          :event="() => colorizeImage()"
                          :iconClass="'fas fa-paint-roller fa-lg'"/>
                    <Tool v-if="!!imageUrl"
                          :key="imageUrl"
                          :event="() => saveImageVersion()"
                          :iconClass="'fas fa-save fa-lg'"/>
                </div>
                <div class="editor">
                    <Editor class="editor-panel editor-canvas"
                            :canvasWidth="canvasWidth"
                            :canvasHeight="canvasHeight"
                            ref="editor"
                    />
                    <Chrome class="editor-panel" :value="color"
                            @input="changeColor"></Chrome>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios";
    import Editor from "vue-image-markup";
    import Tool from "./editor/Tool";
    import ColorPicker from "./editor/ColorPicker";
    import "@fortawesome/fontawesome-free/css/all.css";
    import "@fortawesome/fontawesome-free/js/all.js";
    import {localization} from "../localization/localization";
    import {Chrome} from "vue-color"
    import filepath from "../helpers/filepath";


    export default {
        name: "app",
        components: {
            ColorPicker,
            Tool,
            Editor,
            Chrome
        },
        data() {
            return {
                currentActiveMethod: null,
                params: {},
                imageData: {},
                color: "black",
                imageUrl: null,
                croppedImage: false,
                originalImage: null,
                paintedImage: null,
                projectTitle: ""
            };
        },
        props: {
            canvasWidth: {
                default: 300,
            },
            canvasHeight: {
                default: 300,
            },
            event: {
                type: Function,
            },
            labelForUploadImage: {
                type: Boolean,
                default: false
            },
            iconClass: {
                type: String,
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
        async mounted() {
            let fileId = this.$route.params.file_id;
            if (!!fileId) {
                this.imageData = await this.getImage(fileId);
                this.projectTitle = this.imageData.title;
                this.imageUrl = filepath.getFilepath(this.imageData.filepath);
            }
            if (this.imageUrl) {
                this.$refs.editor.setBackgroundImage(this.imageUrl);
                this.croppedImage = this.$refs.editor.croppedImage;
            }
            this.$watch(
                () => {
                    return this.$refs.editor.croppedImage;
                },
                val => {
                    this.croppedImage = val;
                },
            );
        },
        methods: {
            cropImage() {
                this.currentActiveMethod = "crop";
                this.setTool("crop");
            },
            applyCropping() {
                this.currentActiveMethod = "";
                this.$refs.editor.applyCropping();
            },
            changeColor(color) {
                const colorHex = color.hex;
                this.color = colorHex;
                this.$refs.editor.$data.color = colorHex;
                this.setTool(this.currentActiveMethod);
            },
            saveImage() {
                let image = this.$refs.editor.saveImage();
                this.saveImageAsFile(image);
            },
            saveImageAsFile(base64) {
                let link = document.createElement("a");
                link.setAttribute("href", base64);
                link.setAttribute("download", "image-markup");
                link.click();
            },
            dataURItoFile(dataURI, filename) {
                let byteString = null;
                if (dataURI.split(',')[0].indexOf('base64') >= 0) {
                    byteString = atob(dataURI.split(',')[1]);
                } else {
                    byteString = unescape(dataURI.split(',')[1]);
                }
                let mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

                let ia = new Uint8Array(byteString.length);
                for (let i = 0; i < byteString.length; ++i) {
                    ia[i] = byteString.charCodeAt(i);
                }

                let data = new Blob([ia], {type: mimeString});
                let file = new File([data], filename);
                return file;
            },
            async colorizeImage() {
                if (this.originalImage == null) {
                    console.log("You don't have an original image");
                    return
                }
                let image = this.$refs.editor.saveImage();
                let file = this.dataURItoFile(image, this.originalImage.name);
                let fd = new FormData(document.forms[0]);

                fd.append("originalImage", this.originalImage);
                fd.append("paintedImage", file);
                fd.append("projectTitle", this.projectTitle);
                const response = await axios.post("/api/colorize_file/", fd, {
                    headers: {"Content-Type": "multipart/form-data"}
                });
                await this.$router.push({name: 'images'});
            },
            setTool(type, params) {
                this.currentActiveMethod = type;
                this.$refs.editor.set(type, params);
            },
            sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            },
            async getImage(file_id) {
                const response = await axios.get(
                    `/api/images/${file_id}/`,
                    {
                        headers: {
                            'Access-Control-Allow-Origin': '*',
                        }
                    });
                return response.data || {};
            },
            async uploadImage(e) {
                this.$refs.editor.uploadImage(e);
                this.originalImage = e.target.files[0];
                await this.sleep(2000);
                let image = this.$refs.editor.saveImage();
                this.originalImage = this.dataURItoFile(image, this.originalImage.name);
            },
            async saveImageVersion(e) {
                let image = this.$refs.editor.saveImage();
                let file = this.dataURItoFile(image, this.imageData.filename);
                let fd = new FormData(document.forms[0]);

                fd.append("file", file);
                fd.append("fileId", this.$route.params.file_id);
                fd.append("projectTitle", this.projectTitle);
                const response = await axios.post("/api/save_file/", fd, {
                    headers: {"Content-Type": "multipart/form-data"}
                });
                await this.$router.push({
                    name: 'images',
                    params: {id: this.imageData._id}
                });
            },
            clear() {
                this.currentActiveMethod = this.clear;
                this.$refs.editor.clear();
            },
            undo() {
                this.currentActiveMethod = this.undo;
                this.$refs.editor.undo();
            },
            redo() {
                this.currentActiveMethod = this.redo;
                this.$refs.editor.redo();
            },
        },
    };
</script>

<style>
    .main {
        font-family: "Avenir", Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 50px;
        display: flex;
        justify-content: center;
    }

    .main .editor-container {
        display: flex;
        flex-direction: column;
    }

    .main .editor-container .editor {
        display: flex;
        justify-content: space-between;
    }

    .main .editor-container .editor .current-color {
        border-radius: 5px;
        min-width: 28px;
        min-height: 28px;
    }

    .editor-panel {
        margin-top: 20px;
    }

    .editor-canvas {
        margin-right: 20px;
    }

    canvas {
        border: 1px solid #00000021;
    }
</style>>
