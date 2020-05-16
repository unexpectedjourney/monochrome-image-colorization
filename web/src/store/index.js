import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    enLocalization: true
  },
  getters: {
    getLocalization(state) {
      return state.enLocalization
    }
  },
  mutations: {
    changeLoc(state) {
      state.enLocalization = !state.enLocalization
    }
  },
  actions: {
    changeLocalization(context) {
      context.commit('changeLoc')
    }
  }
})
