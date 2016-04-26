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

from django.core.cache import cache
from gtts import gTTS
from mysite.settings import PREFIX_PATH
import random
import string

def audio_code():
	UUID = []
	for i in range(32):
		UUID.append(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'], 1)[0])
	UUID = string.join(UUID).replace(' ','')
	text = string.join(random.sample(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'], 5), ',')
	tts = gTTS(text=text, lang='en')
	tts.save(PREFIX_PATH +'static/audio_code/' +UUID +'.mp3')
	code = text.replace(',', '')
	cache.set(UUID, code)
	return [UUID, code]

if __name__ == '__main__':
	[UUID, code] = text = audio_code()
	print 'UUID:' +UUID +'\ncode:' +code