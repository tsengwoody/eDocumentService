Vue.use(Vuex)

store = new Vuex.Store({
	state: {
		user: {},
	},
	mutations: {
		updateUser (state, payload) {
				state.user = payload;
		},
	},
	actions: {
		getUser({commit}){
			genericUserAPI.userRest.read(1).then(response => commit('updateUser', response.data))
		},
	},
});
