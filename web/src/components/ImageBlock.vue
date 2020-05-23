<template>
    <div class="col-xs-6 col-sm-4 col-md-4 col-lg-4 text-center"
         style="margin-top:7px;margin-bottom:7px;">
        <router-link :to="{name: 'image', params: { id: image._id }}" class="d-block mb-6 image-link">
            <img class="rounded img-fluid"
                 :src="getFilepath()"
                 width="300" height="300">
            <h3 class="text-center image-link-text">{{image.title || "Your project"}}</h3>
        </router-link>
    </div>
</template>

<script>
    export default {
        name: "Image",
        props: ['image'],
        methods: {
            getFilepath() {
                if (!this.image.filepath) {
                    return "https://i.pinimg.com/originals/10/b2/f6/10b2f6d95195994fca386842dae53bb2.png"
                }
                return "http://localhost/" + this.image.filepath
            }
        }
    }
</script>

<style scoped>

</style>