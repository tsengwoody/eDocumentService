import { create_rest, create_resource, host, file_resolve } from './base.js';

const announcement = axios.create({
	baseURL: host +'genericUser/api/announcements/'
});
export const announcementRest = create_rest(announcement);
