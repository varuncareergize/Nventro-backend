from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Part, PartUsage, PartTransaction
from .serializers import PartSerializer, PartUsageSerializer, PartTransactionSerializer

class PartListView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    """
    API view to list all parts or create a new part.
    """

    def get(self, request):
        parts = Part.objects.all()
        serializer = PartSerializer(parts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PartDetailView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    """
    API view to retrieve, update, or delete a specific part.
    """

    def get_object(self, pk):
        try:
            return Part.objects.get(pk=pk)
        except Part.DoesNotExist:
            return None

    def get(self, request, pk):
        part = self.get_object(pk)
        if not part:
            return Response({'error': 'Part not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PartSerializer(part, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        part = self.get_object(pk)
        if not part:
            return Response({'error': 'Part not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PartSerializer(part, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        part = self.get_object(pk)
        if not part:
            return Response({'error': 'Part not found'}, status=status.HTTP_404_NOT_FOUND)
        part.delete()
        return Response({'message': 'Part deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        """Partial update for a specific part"""
        part = self.get_object(pk)
        if not part:
            return Response({'error': 'Part not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PartSerializer(part, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PartUsageListView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    """
    API view to list or record part usage.
    """
    def get(self, request):
        usages = PartUsage.objects.all().order_by('-used_date')
        serializer = PartUsageSerializer(usages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PartUsageSerializer(data=request.data)
        if serializer.is_valid():
            part = serializer.validated_data['part']
            quantity = serializer.validated_data['quantity_used']

            # Check stock availability
            if part.stock_quantity < quantity:
                return Response(
                    {"error": f"Insufficient stock. Only {part.stock_quantity} units available."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                usage = serializer.save()
                
                # Update stock level
                part.stock_quantity -= quantity
                part.save()
                
                # Automatically log a transaction for history
                PartTransaction.objects.create(
                    part=part,
                    transaction_type='USED',
                    quantity=quantity,
                    remarks=f"Usage for {usage.vehicle.vehicle_name}. Tech: {usage.technician_name}"
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PartTransactionListView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    """
    API view to list or record part transactions.
    """
    def get(self, request):
        transactions = PartTransaction.objects.all().order_by('-created_at')
        serializer = PartTransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PartTransactionSerializer(data=request.data)
        if serializer.is_valid():
            part = serializer.validated_data['part']
            qty = serializer.validated_data['quantity']
            t_type = serializer.validated_data['transaction_type']

            with transaction.atomic():
                if t_type == 'PURCHASE':
                    part.stock_quantity += qty
                elif t_type == 'USED':
                    if part.stock_quantity < qty:
                        return Response(
                            {"error": "Insufficient stock to complete this transaction."}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    part.stock_quantity -= qty
                elif t_type == 'ADJUSTMENT':
                    # Manual override of stock count
                    part.stock_quantity = qty
                
                part.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
