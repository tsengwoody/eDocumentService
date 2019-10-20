from rest_framework import serializers
from .models import *

class BookInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookInfo
		fields = '__all__'

class EditRecordSerializer(serializers.ModelSerializer):
	#editor_name = serializers.ReadOnlyField(read_only=True)
	class Meta:
		model = EditRecord
		exclude = ('edit', 'finish',)

class EBookSerializer(serializers.ModelSerializer):
	bookname = serializers.ReadOnlyField(source='book.book_info.bookname')
	current_editrecord = EditRecordSerializer(read_only=True)
	editrecord_set = EditRecordSerializer(many=True, read_only=True)
	scan_image = serializers.ReadOnlyField(source='get_source_list')

	class Meta:
		model = EBook
		fields = [
			'bookname',
			'current_editrecord',
			'editrecord_set',
			'scan_image',
			'ISBN_part',
			'book',
			'part',
			'edited_page',
			'number_of_times',
			'deadline',
			'get_date',
			'status',
			'service_hours',
		]

class BookSimpleSerializer(serializers.ModelSerializer):
	book_info = BookInfoSerializer(read_only=True)

	class Meta:
		model = Book
		fields = [
			'ISBN',
			'book_info',
			'finish_date',
			'upload_date',
			'priority',
			'scaner',
			'owner',
			'source',
			'status',
			'category',
		]

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
			'category',
		]

class BookAddSerializer(BookSerializer):
	ebook_set = EBookSerializer(many=True, read_only=True)

class BookOrderSerializer(serializers.ModelSerializer):
	bookname = serializers.ReadOnlyField(source='book.book_info.bookname')
	status = serializers.ReadOnlyField(source='book.status')
	class Meta:
		model = BookOrder
		fields = ('__all__')

class LibraryRecordSerializer(serializers.ModelSerializer):
	object = BookSerializer(read_only=True,)
	class Meta:
		model = LibraryRecord
		fields = ('__all__')

class CategorySerializer(serializers.ModelSerializer):
	book_set = BookSerializer(many=True, read_only=True)
	class Meta:
		model = Category
		fields = ('__all__')

#===== ISSN Book =====

class ISSNBookSerializer(serializers.ModelSerializer):
	class Meta:
		model = ISSNBook
		fields = ('__all__')

class ISSNBookInfoSerializer(serializers.ModelSerializer):
	issnbook_set = ISSNBookSerializer(many=True, read_only=True)
	class Meta:
		model = ISSNBookInfo
		fields = '__all__'
