from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    vehicle_image_url = serializers.SerializerMethodField(read_only=True)
    monthly_mileage = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'company',
            'si_no',
            'vehicle_name',
            'vehicle_type',
            'plate_number',
            'vehicle_using_by',
            'service_km',
            'current_km',
            'balance_service_km',
            'model_name',
            'ards_status',
            'insurance_upto',
            'registration_upto',
            'vehicle_image',
            'vehicle_image_url',
            'remarks',
            'created_at',
        ]
        read_only_fields = ['id', 'vehicle_image_url', 'created_at']

    def get_vehicle_image_url(self, obj):
        if not obj.vehicle_image:
            return None

        request = self.context.get('request')
        url = obj.vehicle_image.url
        if request:
            return request.build_absolute_uri(url)
        return url

    def get_monthly_mileage(self, obj):
        return obj.current_km - obj.service_km
