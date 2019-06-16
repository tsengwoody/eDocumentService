import { create_rest, create_resource, host, file_resolve } from './base.js';

const user = axios.create({
	baseURL: host +'genericUser/api/users/'
});

const disabilityCard = axios.create({
	baseURL: host +'genericUser/api/disabilitycards/'
});

const serviceInfo = axios.create({
	baseURL: host +'genericUser/api/serviceinfos/'
});

const announcement = axios.create({
	baseURL: host +'genericUser/api/announcements/'
});

const qAndA = axios.create({
	baseURL: host +'genericUser/api/qandas/'
});

const organization = axios.create({
	baseURL: host +'genericUser/api/organizations/'
});

const businessContent = axios.create({
	baseURL: host +'genericUser/api/businesscontents/'
});

const bannerContent = axios.create({
	baseURL: host +'genericUser/api/bannercontents/'
});

export const userRest = create_rest(user);
export const disabilityCardRest = create_rest(disabilityCard);
export const serviceInfoRest = create_rest(serviceInfo);
export const announcementRest = create_rest(announcement);
export const qAndARest = create_rest(qAndA);
export const organizationRest = create_rest(organization);
export const businessContentRest = create_rest(businessContent);
export const bannerContentRest = create_rest(bannerContent);

export const userAction = {
	login: (username, password) => user.post('action/login/', {username, password,}),
	resetPassword: ({action, username, birthday,}) => user.post('action/retrieve_up/', {action, username, birthday,}),
	getUser: ({action, email, birthday,}) => user.post('action/retrieve_up/', {action, email, birthday,}),
	email: ({category, subject, body,}) => user.post('action/email/', {category, subject, body,}),
}