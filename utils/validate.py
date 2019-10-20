# coding: utf-8
import os
import codecs

def validate_folder(OCR, source, page_per_part):
	OCRFileList = []
	sourceFileList = []
	try:
		OCRFileList = os.listdir(OCR)
		for file in OCRFileList:
			with codecs.open(os.path.join(OCR, file), 'r', encoding='utf-8') as fileRead:
				content=fileRead.read()
		sourceFileList=os.listdir(source)
	except BaseException as e:
		raise e
	page_count = 0
	for scanPage in sourceFileList:
		if scanPage.split('.')[-1].lower() == 'jpg':
			page_count = page_count + 1
	part_count = int((page_count-1)/page_per_part) +1
	for i in range(part_count):
		if u'part{0}.txt'.format(i+1) not in OCRFileList:
			raise OSError('invalid folder')
