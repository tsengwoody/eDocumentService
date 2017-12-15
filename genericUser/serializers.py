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

from ebookSystem.models import EditRecord
class ServiceInfoSerializer(serializers.ModelSerializer):
	editrecord_set = serializers.PrimaryKeyRelatedField(many=True, queryset=EditRecord.objects.filter(serviceInfo=None))
	class Meta:
		model = ServiceInfo
		fields = '__all__'

#	def create(self, validated_data):
#		instance = super(ServiceInfoSerializer, self).create(validated_data)
#		print type(validated_data)

class AnnouncementSerializer(serializers.ModelSerializer):
	class Meta:
		model = Announcement
		fields = ('__all__')

class QAndASerializer(serializers.ModelSerializer):
	class Meta:
		model = QAndA
		fields = ('__all__')

class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organization
		fields = ('__all__')
