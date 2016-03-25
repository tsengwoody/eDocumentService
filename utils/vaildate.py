# coding: utf-8
import os
def vaildate_folder(OCR, source, page_per_part):
	partList = []
	OCRFileList = []
	sourceFileList = []
	try:
		OCRFileList = os.listdir(OCR)
		sourceFileList=os.listdir(source)
	except:
		return False
	page_count = 0
	for scanPage in sourceFileList:
		if scanPage.split('.')[-1].lower() == 'jpg':
			page_count = page_count + 1
	part_count = page_count/page_per_part+1
	for i in range(part_count):
		partList.append('part{}.{}'.format(i+1, 'txt'))
	partSet = set(partList)
	for i in range(i):
		OCRFileList[i] = OCRFileList[i].lower()
	OCRFileSet = set(OCRFileList)
	return [partSet.issubset(OCRFileSet), page_count, part_count]

if __name__ == '__main__':
	print '遠山的回音'
	print vaildate_folder(u'/django/eDocumentService/static/ebookSystem/document/遠山的回音/OCR', u'/django/eDocumentService/static/ebookSystem/document/遠山的回音/source', 50)
	print '藍色駭客'
	print vaildate_folder(u'/django/eDocumentService/static/ebookSystem/document/藍色駭客/OCR', u'/django/eDocumentService/static/ebookSystem/document/藍色駭客/source', 50)