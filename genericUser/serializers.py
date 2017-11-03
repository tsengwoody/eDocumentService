from rest_framework import serializers
from .models import *

class QAndASerializer(serializers.ModelSerializer):
	class Meta:
		model = QAndA
		fields = ('__all__')