<template>
    <div id="app">
        <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
            <router-link to="/" class="navbar-brand">Colorization</router-link>
            <button class="navbar-toggler" type="button" data-toggle="collapse"
                    data-target="#navbarCollapse"
                    aria-controls="navbarCollapse" aria-expanded="false"
                    aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarCollapse">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <router-link class="nav-link" :to="{name: 'home'}">
                            {{getLang.home}}<span
                                class="sr-only">(current)</span></router-link>
                    </li>
                    <li class="nav-item" v-if="loggedIn">
                        <router-link class="nav-link"
                                     :to="{ name: 'image_editor' }">
                            {{getLang.newProject}}
                        </router-link>
                    </li>
                </ul>
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <button type="button" class="btn btn-outline-secondary"
                                v-on:click="changeLocalization"
                                v-if="getLang.flag">English
                        </button>
                        <button type="button" class="btn btn-outline-secondary"
                                v-on:click="changeLocalization"
                                v-if="!getLang.flag">Українська
                        </button>
                    </li>
                    <li class="nav-item dropdown mr-5" v-if="loggedIn">
                        <a class="nav-link dropdown-toggle" href="#"
                           id="navbarDropdown" role="button"
                           data-toggle="dropdown" aria-haspopup="true"
                           aria-expanded="false">
                            {{getLang.user}}
                        </a>
                        <div class="dropdown-menu"
                             aria-labelledby="navbarDropdown">
                            <router-link class="dropdown-item"
                                         :to="{ name: 'user_profile' }">
                                {{getLang.yourProfile}}
                            </router-link>
                            <router-link class="dropdown-item"
                                         :to="{ name: 'images' }">
                                {{getLang.yourProjects}}
                            </router-link>
                            <router-link class="dropdown-item"
                                         :to="{ name: 'user_history' }">
                                {{getLang.yourHistory}}
                            </router-link>
                            <div class="dropdown-divider"></div>
                            <router-link class="dropdown-item"
                                         :to="{ name: 'logout' }">
                                {{getLang.logout}}
                            </router-link>
                        </div>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link"
                                     :to="{ name: 'register' }"
                                     v-if="!loggedIn">{{getLang.register}}
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{ name: 'login' }"
                                     v-if="!loggedIn">{{getLang.login}}
                        </router-link>
                    </li>
                </ul>
            </div>
        </nav>
        <div class="container">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    import accessToken from "./helpers/access-token";
    import {loginTest} from "./helpers/login-test";
    import {mapActions} from "vuex";
    import {localization} from "./localization/localization";

    export default {
        data: () => ({
            loggedIn: false
        }),
        async created() {
            await this.getToken();
        },
        async updated() {
            await this.getToken();
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
            ...mapActions(['changeLocalization']),
            async getToken() {
                await loginTest();
                this.loggedIn = !!accessToken.getToken();
            }
        }
    }
</script>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
    }

    #nav {
        padding: 30px;
    }

    #nav a {
        font-weight: bold;
        color: #2c3e50;
    }

    #nav a.router-link-exact-active {
        color: #42b983;
    }

    .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }

    @media (min-width: 768px) {
        .bd-placeholder-img-lg {
            font-size: 3.5rem;
        }
    }
</style>
