import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token : '',
    username :'',
    playUrl : '',
    tp : 0
  },
  mutations: {
    updateLoginState(state, payload) {
      state.token = payload.token
      state.username = payload.username
    },
    updatePlayUrl(state, payload) {
      state.playUrl = payload.playUrl
      state.tp = payload.tp
    }
  },
  actions: {
  },
  modules: {
  }
})
