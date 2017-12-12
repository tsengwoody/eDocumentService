from rest_framework import serializers
from .models import *

class BookInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookInfo
		fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
	ebook_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	book_info = BookInfoSerializer(read_only=True)
	finish_page_count = serializers.ReadOnlyField(source='collect_finish_page_count')
	finish_part_count = serializers.ReadOnlyField(source='collect_finish_part_count')
	service_hours = serializers.ReadOnlyField(source='collect_service_hours')

	class Meta:
		model = Book
		fields = [
			'ISBN',
			'book_info',
			'ebook_set',
			'page_count',
			'part_count',
			'finish_date',
			'upload_date',
			'priority',
			'scaner',
			'owner',
			'source',
			'status',
			'finish_page_count',
			'finish_part_count',
			'service_hours',
		]

class EBookSerializer(serializers.ModelSerializer):
	scan_image = serializers.ReadOnlyField(source='get_source_list')
	class Meta:
		model = EBook
		fields = [
			'scan_image',
			'ISBN_part',
			'book',
			'part',
			'edited_page',
			'number_of_times',
			'status',
		]

class EditRecordSerializer(serializers.ModelSerializer):
	class Meta:
		model = EditRecord
		fields = '__all__'
