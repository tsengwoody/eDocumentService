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
			'is_license',
			'is_active',
			'is_editor',
			'is_guest',
			'is_manager',
			'auth_email',
			'auth_phone',
		]

class DisabilityCardSerializer(serializers.ModelSerializer):
	class Meta:
		model = DisabilityCard
		fields = '__all__'

from ebookSystem.models import EditRecord
from ebookSystem.serializers import EditRecordSerializer
class ServiceInfoSerializer(serializers.ModelSerializer):
	editrecord_set = serializers.PrimaryKeyRelatedField(many=True, queryset=EditRecord.objects.filter(serviceInfo=None))
	class Meta:
		model = ServiceInfo
		fields = '__all__'

class ServiceInfoAddSerializer(ServiceInfoSerializer):
	editrecordinfo_set = EditRecordSerializer(many=True, read_only=True, source='editrecord_set')
	userinfo = UserSerializer(read_only=True, source='user')

class AnnouncementSerializer(serializers.ModelSerializer):
	class Meta:
		model = Announcement
		fields = ('__all__')

class QAndASerializer(serializers.ModelSerializer):
	order = serializers.ReadOnlyField()

	class Meta:
		model = QAndA
		fields = ('__all__')

class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organization
		fields = ('__all__')

class BannerContentSerializer(serializers.ModelSerializer):
	id = serializers.ReadOnlyField()
	order = serializers.ReadOnlyField()

	class Meta:
		model = BannerContent
		fields = ('__all__')
