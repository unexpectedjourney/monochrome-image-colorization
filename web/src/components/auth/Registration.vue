<template>
    <div class="form-signin">
        <h2 class="login-heading">{{getLang.register}}</h2>
        <form action="#" @submit.prevent="register" method="post">

            <div class="form-label-group">
                <input type="text" id="inputUsername" class="form-control" :placeholder="[[ getLang.username ]]" v-model="username" required autofocus>
                <label for="inputUsername">{{getLang.username}}</label>
            </div>

             <div class="form-label-group">
                <input type="email" id="inputEmail" class="form-control" :placeholder="[[ getLang.email ]]" v-model="email" required>
                <label for="inputEmail">{{getLang.email}}</label>
            </div>

            <div class="form-label-group">
                <input type="password" id="inputPassword1" class="form-control" :placeholder="[[ getLang.password ]]" v-model="password1" required>
                <label for="inputPassword1">{{getLang.password}}</label>
            </div>


            <div class="form-label-group">
                <input type="password" id="inputPassword2" class="form-control" :placeholder="[[ getLang.password ]]" v-model="password2" required>
                <label for="inputPassword2">{{getLang.password}}</label>
            </div>

            <button class="btn btn-lg btn-primary btn-block" type="submit">{{getLang.register}}</button>


        </form>
    </div>
</template>

<script>
    import axios from "axios";
    import accessToken from "../../helpers/access-token";
    import {localization} from "../../localization/localization";
    export default {
        data() {
            return {
                username: '',
                email: '',
                password1: '',
                password2: '',
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
        methods: {
            register() {
                accessToken.removeToken();
                const response = axios.post('/register/', {
                    username: this.username,
                    email: this.email,
                    password1: this.password1,
                    password2: this.password2,
                }).then(response => {
                    accessToken.setToken(response.data.token);
                }).catch(e => {
                    console.log(e)
                });
                this.$router.push({ name: 'home' })
            }
        }
    }
</script>
