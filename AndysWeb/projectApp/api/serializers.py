from dataclasses import field
from rest_framework.serializers import ModelSerializer
from projectApp.models import Room



class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'