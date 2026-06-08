from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_image_url = serializers.SerializerMethodField(read_only=True)
    monthly_mileage = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'vehicle_name',
            'vehicle_code',
            'plate_number',
            'vehicle_image',
            'vehicle_image_url',
            'vehicle_type',
            'monthly_start_mileage',
            'monthly_end_mileage',
            'monthly_mileage',
            'fuel_level',
            'oil_level',
            'battery_health',
            'assigned_driver',
            'next_service_date',
            'status',
        ]
        read_only_fields = ['id', 'vehicle_image_url', 'monthly_mileage']

    def get_vehicle_image_url(self, obj):
        if not obj.vehicle_image:
            return None

        request = self.context.get('request')
        url = obj.vehicle_image.url
        if request:
            return request.build_absolute_uri(url)
        return url

    def get_monthly_mileage(self, obj):
        return obj.monthly_end_mileage - obj.monthly_start_mileage
