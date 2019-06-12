import { create_rest, create_resource, host, file_resolve } from './base.js';

const book = axios.create({
	baseURL: host +'ebookSystem/api/books/'
});
export const bookRest = create_rest(book);
