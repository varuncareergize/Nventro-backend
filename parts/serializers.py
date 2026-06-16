from rest_framework import serializers
from .models import Part, PartUsage, PartTransaction

class PartSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Part
        fields = [
            'id', 'sku', 'part_name', 'category', 'description', 
            'image', 'image_url', 'stock_quantity', 'minimum_stock', 
            'unit_price', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']

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