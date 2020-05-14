import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import store from './store/index'
import axios from "axios";
import accessToken from "./helpers/access-token";
import {loginTest} from "./helpers/login-test";

window.eventBus = new Vue();
Vue.config.productionTip = false;
axios.defaults.baseURL = 'http://0.0.0.0:8000/api';

axios.interceptors.request.use(config => {
  if (accessToken.getToken()) {
    config.headers['Authorization'] = 'Bearer ' + accessToken.getToken();
  }

  return config;
}, error => {
  return Promise.reject(error);
});


router.beforeEach(async (to, from, next) => {
  await loginTest();

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!accessToken.getToken()) {
      next({
        name: 'login',
      })
    } else {
      console.log(1);
      next()
    }
  } else if (to.matched.some(record => record.meta.requiresVisitor)) {
    if (accessToken.getToken()) {
      next({
        name: 'home',
      })
    } else {
      console.log(2);
      next()
    }
  } else {
    console.log(3);
    next();
  }
});


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
