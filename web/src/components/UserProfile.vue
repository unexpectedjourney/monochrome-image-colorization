<template>
    <div class="container">
        <h2>User info</h2>
        <div v-if="isUpdating">
            <div class="form-label-group">
                <input type="text" id="inputUsername"
                       class="form-control text-center" placeholder="Username"
                       v-model="user.username" disabled>
                <label for="inputUsername">Username</label>
            </div>
            <div class="form-label-group">
                <input type="text" id="inputFirstname"
                       class="form-control text-center"
                       placeholder="First name" v-model="user.first_name"
                       autofocus>
                <label for="inputFirstname">First name</label>
            </div>
            <div class="form-label-group">
                <input type="text" id="inputLastname"
                       class="form-control text-center" placeholder="Last name"
                       v-model="user.last_name">
                <label for="inputUsername">Last name</label>
            </div>
            <div class="form-label-group">
                <input type="email" id="inputEmail"
                       class="form-control text-center" placeholder="Email"
                       v-model="user.email" required>
                <label for="inputUsername">Email</label>
            </div>
            <div>
                <button type="button" class="btn btn-success edit_button"
                        v-on:click="updateUser()">Save
                </button>
                <button type="button" class="btn btn-danger"
                        v-on:click="isUpdating=false">Cancel
                </button>
            </div>
        </div>
        <div v-else>
            <h3>Username</h3>
            <h4>{{user.username || "--"}}</h4>
            <h3>First name</h3>
            <h4>{{user.first_name || "--"}}</h4>
            <h3>Last name</h3>
            <h4>{{user.last_name || "--"}}</h4>
            <h3>Email</h3>
            <h4>{{user.email || "--"}}</h4>
            <div>
                <button type="button" class="btn btn-success"
                        v-on:click="isUpdating=true">Edit
                </button>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from "axios"

    export default {
        name: "UserProfile",
        data: () => ({
            user: {
                first_name: '',
                last_name: '',
                email: '',
                username: ''
            },
            isUpdating: false
        }),
        async created() {
            this.user = await this.getUserData();
        },
        methods: {
            async getUserData() {
                let response = await axios.get("/api/users/")
                return response.data || {}
            },
            async updateUser() {
                let data = {
                    first_name: this.user.first_name,
                    last_name: this.user.last_name,
                    email: this.user.email,
                }
                let response = await axios.put(`/api/users/${this.user._id}`, data, {
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                    }
                })
                this.user = response.data || {}
                this.isUpdating = false
            }
        }
    }
</script>

<style scoped>
    .edit_button {
        margin-right: 3px;
    }
</style>