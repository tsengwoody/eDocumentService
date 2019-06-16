import { create_rest, create_resource, host, file_resolve } from './base.js';

const bookSimple = axios.create({
	baseURL: host +'ebookSystem/api/booksimples/'
});

const book = axios.create({
	baseURL: host +'ebookSystem/api/books/'
});

const bookAdd = axios.create({
	baseURL: host +'ebookSystem/api/bookadds/'
});

const ebook = axios.create({
	baseURL: host +'ebookSystem/api/ebooks/'
});

const bookInfo = axios.create({
	baseURL: host +'ebookSystem/api/bookinfos/'
});

const bookOrder = axios.create({
	baseURL: host +'ebookSystem/api/bookorders/'
});

const editRecord = axios.create({
	baseURL: host +'ebookSystem/api/editrecords/'
});

const libraryRecord = axios.create({
	baseURL: host +'ebookSystem/api/libraryrecords/'
});

const category = axios.create({
	baseURL: host +'ebookSystem/api/categorys/'
});

export const bookSimpleRest = create_rest(bookSimple);
export const bookRest = create_rest(book);
export const bookAddRest = create_rest(bookAdd);
export const ebookRest = create_rest(ebook);
export const bookInfoRest = create_rest(bookInfo);
export const bookOrderRest = create_rest(bookOrder);
export const editRecordRest = create_rest(editRecord);
export const libraryRecordRest = create_rest(libraryRecord);
export const categoryRest = create_rest(category);

export const libraryRecordAction = {
	checkInout: ({pk, action,}) => libraryRecord.post(`${pk}/action/check_inout/`, {action,}),
}