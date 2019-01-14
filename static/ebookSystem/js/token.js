/* 
js-cookie
jquery
jwt-decode
*/

'use strict';

function o2j(v) {
	//物件轉json文字

	let c = '';
	try {
		//c = JSON.stringify(v);
		c = JSON.stringify(v, null, '\t');
	}
	catch (err) {
	}

	return c;
}

function j2o(v) {
	//json文字轉物件

	let c = {};
	try {
		c = JSON.parse(v);
	}
	catch (err) {
	}

	return c;
}

function get_token_exp_time(token){
	let token_obj = jwt_decode(token);
	token_obj['exp_date'] = new Date(token_obj.exp*1000)
	return token_obj['exp_date'] - Date.now();
}

function check_token_exp(token){
	let exp_second = get_token_exp_time(token)/1000;
	if(exp_second > 0){
		return false;
	}
	else {
		return true;
	}
}

function check_token_exp_come soon(token, period_second){
	let exp_second = get_token_exp_time(token)/1000;
	if(exp_second > 0 && exp_second - period_second < 0){
		return true;
	}
	else {
		return false;
	}
}

function get_user_id_from_token(token){
	let token_obj = jwt_decode(token);
	return token_obj.user_id;
}

function get_refresh_token(token) {
	//df
	let df = $.Deferred();

	//ajax
	$.ajax({
		url: '/api-token-refresh/',
		type: 'post',
		data: {'token': token},
		//contentType: 'application/json', //default: 'application/x-www-form-urlencoded; charset=UTF-8'
		'error': function (xhr) {
			let res = {
				'status': xhr.status,
				'responseText': xhr.responseText,
			};

			df.reject(res);

		},
		success: function(data, textStatus, xhr) {
			let res = data;

			df.resolve(res);

		}
	})

	return df;

}

function get_token(username, password) {
	//df
	let df = $.Deferred();

	//ajax
	$.ajax({
		url: '/api-token-auth/',
		type: 'post',
		data: {
			'username': username,
			'password': password,
		},
		//contentType: 'application/json', //default: 'application/x-www-form-urlencoded; charset=UTF-8'
		'error': function (xhr) {
			let res = {
				'status': xhr.status,
				'responseText': xhr.responseText,
			};

			df.reject(res);

		},
		success: function(data, textStatus, xhr) {
			let res = data;

			df.resolve(res);

		}
	})

	return df;

}

$(document).ready(function () {
	let period_second = 3600;
	let period_time = period_second * 1000;
	setInterval(function () {

	}, period_time);

});
