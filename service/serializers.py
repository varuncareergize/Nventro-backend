from rest_framework import serializers
from .models import VehicleService, ServiceDocument, ServicePart


class VehicleServiceSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VehicleService
        fields = [
            'id', 'vehicle', 'vehicle_name', 'service_date', 'odometer_reading', 'service_type',
            'estimated_cost', 'actual_cost', 'work_performed', 'breakdown_details',
            'accident_details', 'workshop_name', 'next_service_due_km',
            'next_service_date', 'vehicle_downtime_days', 'remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'vehicle_name', 'created_at', 'updated_at']

    def get_vehicle_name(self, obj):
        return obj.vehicle.vehicle_name if obj.vehicle else None


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
    part = serializers.SerializerMethodField(read_only=True)
    vehicle = serializers.SerializerMethodField(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)
    qty = serializers.SerializerMethodField(read_only=True)
    tech = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ServicePart
        fields = ['id', 'part', 'vehicle', 'date', 'qty', 'tech']
        read_only_fields = ['id', 'part', 'vehicle', 'date', 'qty', 'tech']

    def get_part(self, obj):
        return obj.part.part_name if obj.part else None

    def get_vehicle(self, obj):
        return obj.service.vehicle.vehicle_name if obj.service and obj.service.vehicle else None

    def get_date(self, obj):
        return obj.service.service_date.strftime('%b %d, %Y') if obj.service and obj.service.service_date else None

    def get_qty(self, obj):
        return obj.quantity

    def get_tech(self, obj):
        return obj.service.workshop_name if obj.service and obj.service.workshop_name else 'N/A'
