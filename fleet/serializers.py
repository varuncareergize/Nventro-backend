from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id',
            'vehicle_name',
            'vehicle_code',
            'plate_number',
            'vehicle_type',
            'current_mileage',
            'fuel_level',
            'oil_level',
            'battery_health',
            'assigned_driver',
            'next_service_date',
            'status',
        ]
        read_only_fields = ['id']
