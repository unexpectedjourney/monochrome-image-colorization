<template>
  <div id="app" class="main">
    <div class="editor-container">
      <div class="editor">
        <div class="current-color" :style="{ backgroundColor: color }"></div>

        <Tool :event="() => undo()" :iconClass="'fas fa-undo-alt fa-lg'" />

        <Tool :event="() => redo()" :iconClass="'fas fa-redo-alt fa-lg'" />

        <Tool :event="() => clear()" :iconClass="'fas fa-trash-alt fa-lg'" />

        <Tool
          :event="() => setTool('freeDrawing')"
          :iconClass="'fas fa-pencil-alt fa-lg'"
          :class="{ 'active-tool': currentActiveMethod === 'freeDrawing' }"
        />

        <Tool
          :event="() => setTool('text')"
          :iconClass="'fas fa-font fa-lg'"
          :class="{ 'active-tool': currentActiveMethod === 'text' }"
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
          :event="() => cropImage()"
          :iconClass="'fas fa-crop-alt fa-lg'"
          v-show="!croppedImage"
        />

        <Tool
          :event="e => uploadImage(e)"
          :iconClass="'fas fa-file-upload fa-lg'"
          :labelForUploadImage="true"
        />
        <Tool :event="() => saveImage()" :iconClass="'fas fa-save fa-lg'" />
        <Tool :event="() => colorizeImage()" :iconClass="'fas fa-paint-roller'" />
      </div>
      <Editor
        :canvasWidth="canvasWidth"
        :canvasHeight="canvasHeight"
        ref="editor"
      />
    </div>
    <div class="colors">
      <ColorPicker :color="'#e40000'" :event="changeColor" />
      <ColorPicker :color="'#e8eb34'" :event="changeColor" />
      <ColorPicker :color="'#a834eb'" :event="changeColor" />
      <ColorPicker :color="'#65c31a'" :event="changeColor" />
      <ColorPicker :color="'#34b7eb'" :event="changeColor" />
      <ColorPicker :color="'#eb34df'" :event="changeColor" />
      <ColorPicker :color="'#1a10ad'" :event="changeColor" />
      <ColorPicker :color="'#000000'" :event="changeColor" />
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
export default {
  name: "app",
  components: {
    ColorPicker,
    Tool,
    Editor,
  },
  data() {
    return {
      currentActiveMethod: null,
      params: {},
      color: "black",
      imageUrl: null,
      croppedImage: false,
      originalImage: null,
      paintedImage: null,
    };
  },
  props: {
    canvasWidth: {
      default: 600,
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
    },
    canvasHeight: {
      default: 600,
    },
  },
  mounted() {
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
    changeColor(colorHex) {
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
    blobToFile(theBlob, fileName){
      theBlob.lastModifiedDate = new Date();
      theBlob.name = fileName;
      return theBlob;
    },
    dataURItoFile(dataURI, filename) {
        let byteString = null;
        if (dataURI.split(',')[0].indexOf('base64') >= 0) {
          byteString = atob(dataURI.split(',')[1]);
        }
        else {
          byteString = unescape(dataURI.split(',')[1]);
        }
        let mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
        console.log(mimeString);
        // write the bytes of the string to a typed array
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
      const response = await axios.post("/api/colorize_file/", fd, {
        headers: { "Content-Type": "multipart/form-data"}
      });
      console.log(response.status);
    },
    setTool(type, params) {
      this.currentActiveMethod = type;
      this.$refs.editor.set(type, params);
    },
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    async uploadImage(e) {
      this.$refs.editor.uploadImage(e);
      this.originalImage = e.target.files[0];
      console.log(this.originalImage);
      await this.sleep(2000);
      let image = this.$refs.editor.saveImage();
      this.originalImage = this.dataURItoFile(image, this.originalImage.name);
      console.log(this.originalImage);
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
.main .editor-container .editor .active-tool {
  cursor: pointer;
  color: #4287f5;
}
.main .colors {
  display: flex;
  flex-direction: column;
  margin: 40px 25px 0 25px;
  align-items: center;
  justify-content: center;
}

.custom-editor {
  margin-top: 20px;
}

canvas {
  border: 1px solid #00000021;
}
</style>>
