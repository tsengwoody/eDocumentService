	function get_user(source){
		let df = $.Deferred();
		let user_id;
		let user = {};

		if(source==='token'){
			let user_token = Object.create(Token);
			user_token.set('token');
			user_token.load();
			if(user_token.check_active()){
				user_id = user_token.get_user_id();
			}
		}
		else if(source==='session'){
			user_id = $('div[user_id]').attr('user_id');
		}

		user_id = Number(user_id);

		if(user_id){

			let client = new $.RestClient('/genericUser/api/', {
				ajax: {
					async: false,
				},
			});

			client.add('users');

			client.users.read(user_id)
			.done(function (data, textStatus, xhrObject) {
				user = data;
			})
			.fail(function(xhr, result, statusText){
				user = {};
			})

		}
		else {
			user = {}
		}

		return user;

	}

var user;

$(function(){
	user = get_user('session')
})