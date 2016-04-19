# coding: utf-8
import os

def handle_uploaded_file(dirname, file):
	if not os.path.exists(dirname):
		os.makedirs(dirname, 0777)
	fullpath = os.path.join(dirname, file.name)
	if os.path.exists(fullpath):
		return {'status':'error', 'message':u'檔案已存在'}
	with open(fullpath, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)
	return {'status':'success', 'message':u'檔案成功上傳'}