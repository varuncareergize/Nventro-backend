from rest_framework import serializers
from .models import VehicleService, ServiceDocument, ServicePart


class VehicleServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleService
        fields = [
            'id', 'vehicle', 'service_date', 'odometer_reading', 'service_type',
            'estimated_cost', 'actual_cost', 'work_performed', 'breakdown_details',
            'accident_details', 'workshop_name', 'next_service_due_km',
            'next_service_date', 'vehicle_downtime_days', 'remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


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


class ServicePartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePart
        fields = ['id', 'service', 'part', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['id', 'total_price']
