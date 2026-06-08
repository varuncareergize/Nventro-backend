from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleListView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    """
    API view to list all vehicles or create a new vehicle.
    GET: Returns a list of all vehicles
    POST: Creates a new vehicle
    """

    def get(self, request):
        """Get all vehicles"""
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new vehicle"""
        serializer = VehicleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehicleDetailView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    """
    API view to retrieve, update, or delete a specific vehicle.
    GET: Returns vehicle details
    PUT: Updates vehicle details
    DELETE: Deletes a vehicle
    """

    def get_object(self, pk):
        """Get vehicle object by primary key"""
        try:
            return Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return None

    def get(self, request, pk):
        """Get a specific vehicle"""
        vehicle = self.get_object(pk)
        if not vehicle:
            return Response(
                {'error': 'Vehicle not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = VehicleSerializer(vehicle, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update a specific vehicle"""
        vehicle = self.get_object(pk)
        if not vehicle:
            return Response(
                {'error': 'Vehicle not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = VehicleSerializer(vehicle, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a specific vehicle"""
        vehicle = self.get_object(pk)
        if not vehicle:
            return Response(
                {'error': 'Vehicle not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        vehicle.delete()
        return Response(
            {'message': 'Vehicle deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
