from rest_framework import serializers
from .models import (
    VehicleService,
    ServiceItem,
    VehicleServiceItem,
    ServiceDocument,
    Part,
    ServicePart,
)


class VehicleServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleService
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ServiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceItem
        fields = '__all__'
        read_only_fields = ['id']


class VehicleServiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleServiceItem
        fields = '__all__'
        read_only_fields = ['id']


class ServiceDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ServiceDocument
        fields = ['id', 'service', 'file', 'file_url', 'uploaded_at']
        read_only_fields = ['id', 'file_url', 'uploaded_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        if obj.file:
            return obj.file.url
        return None


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'
        read_only_fields = ['id']


class ServicePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePart
        fields = '__all__'
        read_only_fields = ['id']
