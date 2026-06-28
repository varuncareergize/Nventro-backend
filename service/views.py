from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .models import VehicleService, ServiceDocument, ServicePart
from .serializers import (
    VehicleServiceSerializer,
    ServiceDocumentSerializer,
    ServicePartSerializer,
    ServicePartCreateSerializer,
)


class BaseListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    model = None
    serializer_class = None

    def get_queryset(self):
        return self.model.objects.all()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseRetrieveUpdateDeleteAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    model = None
    serializer_class = None

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({'error': f'{self.model.__name__} not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({'error': f'{self.model.__name__} not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(obj, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({'error': f'{self.model.__name__} not found'}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response({'message': f'{self.model.__name__} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class VehicleServiceListView(BaseListCreateAPIView):
    model = VehicleService
    serializer_class = VehicleServiceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        vehicle_id = self.request.query_params.get('vehicle_id')
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        return queryset


class VehicleServiceDetailView(BaseRetrieveUpdateDeleteAPIView):
    model = VehicleService
    serializer_class = VehicleServiceSerializer


class ServiceDocumentListView(BaseListCreateAPIView):
    model = ServiceDocument
    serializer_class = ServiceDocumentSerializer


class ServiceDocumentDetailView(BaseRetrieveUpdateDeleteAPIView):
    model = ServiceDocument
    serializer_class = ServiceDocumentSerializer


class ServicePartListView(BaseListCreateAPIView):
    model = ServicePart
    serializer_class = ServicePartSerializer

    def post(self, request):
        serializer = ServicePartCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            service_part = serializer.save()
            response_serializer = ServicePartSerializer(service_part, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServicePartDetailView(BaseRetrieveUpdateDeleteAPIView):
    model = ServicePart
    serializer_class = ServicePartSerializer
