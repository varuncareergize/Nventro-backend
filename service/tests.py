from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from fleet.models import Company, Vehicle
from .models import VehicleService


class VehicleServiceFilterTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Company', address='Main Street')
        self.vehicle_one = Vehicle.objects.create(
            company=self.company,
            vehicle_name='Bus 101',
            plate_number='ABC-123',
        )
        self.vehicle_two = Vehicle.objects.create(
            company=self.company,
            vehicle_name='Bus 202',
            plate_number='XYZ-789',
        )
        VehicleService.objects.create(
            vehicle=self.vehicle_one,
            service_date='2026-06-01',
            odometer_reading=1000,
            service_type='ROUTINE',
            estimated_cost='100.00',
        )
        VehicleService.objects.create(
            vehicle=self.vehicle_two,
            service_date='2026-06-02',
            odometer_reading=2000,
            service_type='ROUTINE',
            estimated_cost='200.00',
        )

    def test_list_services_filtered_by_vehicle_id(self):
        url = reverse('vehicle-service-list')
        response = self.client.get(url, {'vehicle_id': self.vehicle_one.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['vehicle'], self.vehicle_one.id)
