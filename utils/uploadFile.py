# coding: utf-8
import os

def handle_uploaded_file(dirname, file):
	if not os.path.exists(dirname):
		os.makedirs(dirname, 0770)
	fullpath = os.path.join(dirname, file.name)
	if os.path.exists(fullpath):
		return ['error', u'檔案已存在']
	with open(fullpath, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)
	return ['success', u'檔案成功上傳']

from django.core.files.uploadhandler import FileUploadHandler,    UploadFileException

# class who handles the upload
class ProgressUploadSessionHandler(FileUploadHandler):
    """
    Download the file and store progression in the session
    """
    def __init__(self, request=None, outPath="/tmp"):
        super(ProgressUploadSessionHandler, self).__init__(request)
        self.progress_id = None
        self.cache_key = None
        self.request = request
        self.outPath = outPath
#        self.destination = None

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        self.content_length = content_length
        if 'X-Progress-ID' in self.request.GET :
            self.progress_id = self.request.GET['X-Progress-ID']
        elif 'HTTP_X_PROGRESS_ID' in self.request.META:
            self.progress_id = self.request.META['HTTP_X_PROGRESS_ID']
        if self.progress_id:
            self.cache_key = self.progress_id
            self.request.session['upload_progress_%s' % self.cache_key] =  {
                'length': self.content_length,
                'uploaded' : 0
            }

#    def new_file(self, field_name, file_name, content_type, content_length, charset=None):
        #if not is_valid_upload(file_name):         # here you can use a function to filter uploaded files.
        #    raise    UploadFileException , "forbidden file type" 
#        self.outPath = os.path.join(self.outPath, file_name)
#        self.destination = open(self.outPath, 'wb+')
#        pass

    def receive_data_chunk(self, raw_data, start):
        data = self.request.session['upload_progress_%s' % self.cache_key]
        data['uploaded'] += self.chunk_size
        self.request.session['upload_progress_%s' % self.cache_key] = data
        self.request.session.save()
#        self.destination.write( raw_data)
        # data wont be passed to any other handler
        return raw_data
    
    def file_complete(self, file_size):
        pass

    def upload_complete(self):
#        try:
#            self.destination.close()
#        except:
#            pass
        del self.request.session['upload_progress_%s' % self.cache_key]

from django.core.cache import cache

class UploadProgressCachedHandler(FileUploadHandler):
    """
    Tracks progress for file uploads.
    The http post request must contain a header or query parameter, 'X-Progress-ID'
    which should contain a unique string to identify the upload to be tracked.
    """

    def __init__(self, request=None):
        super(UploadProgressCachedHandler, self).__init__(request)
        self.progress_id = None
        self.cache_key = None

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        self.content_length = content_length
        if 'X-Progress-ID' in self.request.GET :
            self.progress_id = self.request.GET['X-Progress-ID']
        elif 'HTTP_X_PROGRESS_ID' in self.request.META:
            self.progress_id = self.request.META['HTTP_X_PROGRESS_ID']
        
        if self.progress_id:
            self.cache_key = "%s_%s" % (self.request.META['REMOTE_ADDR'], self.progress_id)
            cache.set(self.cache_key, {
                'length': self.content_length,
                'uploaded' : 0
            },30)

    def receive_data_chunk(self, raw_data, start):
        if self.cache_key:
            data = cache.get(self.cache_key)
            data['uploaded'] += self.chunk_size
            cache.set(self.cache_key, data)
        return raw_data
    
    def file_complete(self, file_size):
        pass

    def upload_complete(self):
        if self.cache_key:
            cache.delete(self.cache_key)
