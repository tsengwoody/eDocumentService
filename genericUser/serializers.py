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

class AnnouncementSerializer(serializers.ModelSerializer):
	class Meta:
		model = Announcement
		fields = ('__all__')

class QAndASerializer(serializers.ModelSerializer):
	class Meta:
		model = QAndA
		fields = ('__all__')
