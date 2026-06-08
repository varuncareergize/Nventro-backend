from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    monthly_mileage = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'vehicle_name',
            'vehicle_code',
            'plate_number',
            'vehicle_image',
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
        read_only_fields = ['id', 'monthly_mileage']

    def get_monthly_mileage(self, obj):
        return obj.monthly_end_mileage - obj.monthly_start_mileage
