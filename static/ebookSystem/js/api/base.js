//import * as _ from "lodash"
//import axios from 'axios';
//import FileSaver from 'file-saver';

export const host = '/';

export const file_resolve = (resource) => {
	return (response) => {
		const url = window.URL.createObjectURL(new Blob([response.data]));
		const link = document.createElement('a');
		// response header Content-Disposition:attachment; filename=elmeast-report-2018-2.pdf
		let head = response.headers['Content-Disposition'];
		let resource_list = resource.split('/');
		let fname = resource_list[resource_list.length-1]
		console.log(fname);
		if (head) {
			try {
				fname = head.split(';')[1].split('=')[1]
			} catch (err){
				console.log(err);
			}
		}

		FileSaver.saveAs(response.data, fname);

		/*link.href = url;
		link.setAttribute('download', fname);
		document.body.appendChild(link);
		link.click();*/
	}
}

export const create_rest = axiosapi => {
	axiosapi.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');
	return {
		options: () => axiosapi.options(''),
		list: () => axiosapi.get(''),
		create: (data) => axiosapi.post('', data),
		read: (pk) => axiosapi.get(`/${pk}/`),
		update: (pk, data) => axiosapi.put(`/${pk}/`, data),
		partialupdate: (pk, data) => axiosapi.patch(`/${pk}/`, data),
		delete: (pk) => axiosapi.delete(`/${pk}/`),
		filter: (filter) => axiosapi.get('', {params: filter}),
	};
};

export const create_resource = axiosapi => {
	return {
		metadatalist: (dir, resource) => axiosapi.get(`/resource/metadata/${dir}/${resource}/`),
		metadatadetail: (pk, dir, resource) => axiosapi.get(`/${pk}/resource/metadata/${dir}/${resource}/`),
		contentdownlist: (dir, resource) => {
			return axiosapi.get(`/resource/content/${dir}/${resource}/`, {responseType: 'blob'})
			.then(file_resolve(resource))
		},
		contentdowndetail: (pk, dir, resource) => {
			return axiosapi.get(`/${pk}/resource/content/${dir}/${resource}/`, {responseType: 'blob'})
			.then(file_resolve(resource))
		},
		/*contentdownlist: (dir, resource) => location.replace(`${axiosapi.defaults.baseURL}/resource/content/${dir}/${resource}/`),
		contentdowndetail: (pk, dir, resource) => location.replace(`${axiosapi.defaults.baseURL}/${pk}/resource/content/${dir}/${resource}/`),*/
		contentuplist: (dir, resource, file) => {
			let formData = new FormData();
			formData.append('object', file);
			return axiosapi.post(`/resource/content/${dir}/${resource}/`, formData, {
				headers: {
					'Content-Type': 'multipart/form-data',
				},
			})
			.then(res => {
				return [dir, resource];
			})
		},
		contentupdetail: (dir, resource, file) => {
			let formData = new FormData();
			formData.append('object', file);
			return axiosapi.post(`/${pk}/resource/content/${dir}/${resource}/`, formData, {
				headers: {
					'Content-Type': 'multipart/form-data',
				},
			})
			.then(res => {
				return [dir, resource];
			})
		},
		contentdeletelist: (dir, resource) => {
			return axiosapi.delete(`/resource/content/${dir}/${resource}/`)
			.then(res => {
				return [dir, resource];
			})
		},
		contentdeletedetail: (pk, dir, resource) => {
			axiosapi.delete(`/${pk}/resource/content/${dir}/${resource}/`)
			.then(res => {
				return [dir, resource];
			})
		},
	};
};

export const create_localrest = key => {
	return {
		list: () => {
			let all;
			if(localStorage.getItem(key)){
				all = JSON.parse(localStorage.getItem(key));
				return all;
			}
			else {
				return [];
			}
		},
		create: (data) => {
			let all;
			if(!localStorage.getItem(key)){
				all = [];
			}
			else {
				all = JSON.parse(localStorage.getItem(key));
			}
			console.log(all);
			data['pk'] = all.length;
			all.push(data);
			localStorage.setItem(key, JSON.stringify(all));
			return data;
		},
		read: (pk) => {
			let temp = {};
			let all = JSON.parse(localStorage.getItem(key));
			all.forEach((v, i)=>  {
				if(v.pk==pk){
					temp = v;
				}
			})
			return temp;
		},
		update: (pk, data) => {
			let temp = {};
			let all = JSON.parse(localStorage.getItem(key));
			all.forEach((v, i)=>  {
				if(v.pk==pk){
					temp = v;
				}
			})
			if(temp){
				_.merge(temp, data);
			}
			return temp;
		},
		partialupdate: (pk, data) => {
		},
		clear: () => {
			localStorage.removeItem(key);
		},
		delete: (pk) => {
			let arr = [];
			let temp = {};
			let all;
			if(localStorage.getItem(key)){
				all = JSON.parse(localStorage.getItem(key));
				all.forEach((v, i)=>  {
					if(v.pk==pk){
						temp = v;
					}
					else {
						arr.push(v);
					}
				})
				localStorage.setItem(key, JSON.stringify(all));
				return temp;
			}
			else {
				return [];
			}
		},
	};
};
