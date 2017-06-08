# coding: utf-8
import os
import codecs

def validate_folder(OCR, source, page_per_part):
	partList = []
	OCRFileList = []
	sourceFileList = []
	try:
		OCRFileList = os.listdir(OCR)
		for file in OCRFileList:
			with codecs.open(os.path.join(OCR, file), 'r', encoding='utf-8') as fileRead:
				content=fileRead.read()
		sourceFileList=os.listdir(source)
	except:
		return [False, None, None]
	page_count = 0
	for scanPage in sourceFileList:
		if scanPage.split('.')[-1].lower() == 'jpg':
			page_count = page_count + 1
	part_count = (page_count-1)/page_per_part+1
	for i in range(part_count):
		partList.append('part{}.{}'.format(i+1, 'txt'))
	partSet = set(partList)
	for i in range(i):
		OCRFileList[i] = OCRFileList[i].lower()
	OCRFileSet = set(OCRFileList)
	return [partSet.issubset(OCRFileSet), page_count, part_count]
