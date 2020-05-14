<template>
    <div class="form-signin">
        <h2 class="login-heading">{{getLang.login}}</h2>
        <form action="#" @submit.prevent="login">
            <div class="form-label-group">
                <input type="email" id="inputEmail" class="form-control" :placeholder="[[ getLang.username ]]" v-model="username" required autofocus>
                <label for="inputEmail">{{getLang.username}}</label>
            </div>

            <div class="form-label-group">
                <input type="password" id="inputPassword" class="form-control" :placeholder="[[ getLang.password ]]" v-model="password" required>
                <label for="inputPassword">{{getLang.password}}</label>
            </div>
            <button class="btn btn-lg btn-primary btn-block" type="submit">{{getLang.login}}</button>
        </form>
    </div>
</template>

<script>
    import axios from 'axios';
    import accessToken from '../../helpers/access-token';
    import {localization} from "../../localization/localization";
    export default {
        name: 'login',
        data() {
            return {
                username: '',
                password: '',
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
            async login() {
                const response = await axios.post('/auth/login/', {
                    username: this.username,
                    password: this.password,
                });
                const token = response.data.token;
                accessToken.setToken(token);
                console.log(token);
                this.$router.push({ name: 'home' });
            }
        }
    }
</script>

<style>
html,
body {
  height: 100%;
}


.form-signin {
  width: 100%;
/*   max-width: 420px;
 */  padding: 15px;
  margin: auto;
}

.form-label-group {
  position: relative;
  margin-bottom: 1rem;
}

.form-label-group > input,
.form-label-group > label {
  height: 3.125rem;
  padding: .75rem;
}

.form-label-group > label {
  position: absolute;
  top: 0;
  left: 0;
  display: block;
  width: 100%;
  margin-bottom: 0; /* Override default `<label>` margin */
  line-height: 1.5;
  color: #495057;
  pointer-events: none;
  cursor: text; /* Match the input under the label */
  border: 1px solid transparent;
  border-radius: .25rem;
  transition: all .1s ease-in-out;
}

.form-label-group input::-webkit-input-placeholder {
  color: transparent;
}

.form-label-group input:-ms-input-placeholder {
  color: transparent;
}

.form-label-group input::-ms-input-placeholder {
  color: transparent;
}

.form-label-group input::-moz-placeholder {
  color: transparent;
}

.form-label-group input::placeholder {
  color: transparent;
}

.form-label-group input:not(:placeholder-shown) {
  padding-top: 1.25rem;
  padding-bottom: .25rem;
}

.form-label-group input:not(:placeholder-shown) ~ label {
  padding-top: .25rem;
  padding-bottom: .25rem;
  font-size: 12px;
  color: #777;
}

/* Fallback for Edge
-------------------------------------------------- */
@supports (-ms-ime-align: auto) {
  .form-label-group > label {
    display: none;
  }
  .form-label-group input::-ms-input-placeholder {
    color: #777;
  }
}

/* Fallback for IE
-------------------------------------------------- */
@media all and (-ms-high-contrast: none), (-ms-high-contrast: active) {
  .form-label-group > label {
    display: none;
  }
  .form-label-group input:-ms-input-placeholder {
    color: #777;
  }
}
</style>
