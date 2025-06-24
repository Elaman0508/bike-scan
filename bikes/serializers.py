from rest_framework import serializers
from .models import BikePhoto

class BikePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikePhoto
        fields = ['id', 'image', 'uploaded_at']
