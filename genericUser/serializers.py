from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'id',
			'username',
			'email',
			'first_name',
			'last_name',
			'phone',
			'birthday',
			'education',
			'is_book',
			'org',
		]

class ServiceInfoSerializer(serializers.ModelSerializer):
	editrecord_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
	class Meta:
		model = ServiceInfo
		fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
	class Meta:
		model = Announcement
		fields = ('__all__')

class QAndASerializer(serializers.ModelSerializer):
	class Meta:
		model = QAndA
		fields = ('__all__')
