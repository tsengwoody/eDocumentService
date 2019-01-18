﻿/* 
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

var Token = {
	set: function set(name){
		this.name = name;
	},
	get: function get(){
		return this.token;
	},
	load: function load(){
		this.token = localStorage.getItem(this.name);
	},
	save: function save(){
		localStorage.setItem(this.name, this.token);
	},
	remove: function remove(){
		localStorage.removeItem(this.name);
	},
	check_token: function check_token(){
		try {
			let token_obj = jwt_decode(this.token);
			return true;
		}
		catch (err) {
			return false;
		}
	},
	get_exp_countdown: function get_exp_countdown(){
		try {
			let token_obj = jwt_decode(this.token);
			token_obj['exp_date'] = new Date(token_obj.exp*1000)
			return token_obj['exp_date'] - Date.now();
		}
		catch (err) {
			return null;
		}
	},
	check_exp: function check_exp(){
		try {
			let exp_second = this.get_exp_countdown()/1000;
			if(exp_second >= 0){
				return false;
			}
			else {
				return true;
			}
		}
		catch (err) {
			return false;
		}
	},
	check_exp_come_soon: function check_exp_come_soon(period_second){
		try {
			let exp_second = this.get_exp_countdown()/1000;
			if(exp_second > 0 && exp_second - period_second < 0){
				return true;
			}
			else {
				return false;
			}
		}
		catch (err) {
			return false;
		}
	},
	check_active: function check_active(){
		try {
			let exp_second = this.get_exp_countdown()/1000;
			if(exp_second > 1){
				return true;
			}
			else {
				console.log(this.get_exp_countdown())
				return false;
			}
		}
		catch (err) {
			return false;
		}
	},
	get_user_id: function get_user_id(){
		try {
			return jwt_decode(this.token).user_id;
		}
		catch (err) {
			return null;
		}
	},
	get_username: function get_user_id(){
		try {
			return jwt_decode(this.token).username;
		}
		catch (err) {
			return null;
		}
	},
	get_exp_date: function get_user_id(){
		try {
			return new Date(jwt_decode(this.token).exp*1000);
		}
		catch (err) {
			return null;
		}
	},
	get_orig_iat_date: function get_user_id(){
		try {
			return new Date(jwt_decode(this.token).orig_iat*1000);
		}
		catch (err) {
			return null;
		}
	},
	refresh: function refresh() {
		//df
		let df = $.Deferred();

		//ajax
		$.ajax({
			url: '/api-token-refresh/',
			type: 'post',
			data: {'token': this.token},
			//contentType: 'application/json', //default: 'application/x-www-form-urlencoded; charset=UTF-8'
			'error': function (xhr) {
				let res = {
					'status': xhr.status,
					'responseText': xhr.responseText,
				};

				df.reject(res);

			},
			success: (data, textStatus, xhr) => {
				let res = data;
				this.token = data['token'];
				df.resolve(res);

			}
		})

		return df;

	},
	obtain: function obtain(username, password) {
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
			success: (data, textStatus, xhr) => {
				let res = data;
				this.token = data['token'];
				df.resolve(res);

			}
		})

		return df;

	},
}

var token = Object.create(Token);
token.set('token');
token.load();
