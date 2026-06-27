from rest_framework import serializers
from .models import Part, PartUsage, PartTransaction

class PartSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Part
        fields = [
            'id', 'part_number', 'part_name', 'category', 'description',
            'image', 'image_url', 'stock_quantity', 'minimum_stock',
            'unit_price', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'image_url']
        extra_kwargs = {
            'part_number': {'required': True},
            'part_name': {'required': True},
            'category': {'required': True},
            'stock_quantity': {'required': True},
            'minimum_stock': {'required': True},
            'unit_price': {'required': True},
        }

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock quantity cannot be negative.')
        return value

    def validate_minimum_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Minimum stock cannot be negative.')
        return value

    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Unit price cannot be negative.')
        return value

    def get_image_url(self, obj):
        if not obj.image:
            return None

        request = self.context.get('request')
        url = obj.image.url
        if request:
            return request.build_absolute_uri(url)
        return url

class PartUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartUsage
        fields = '__all__'

class PartTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartTransaction
        fields = '__all__'