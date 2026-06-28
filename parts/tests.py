from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Part


class PartCreateTests(APITestCase):
    def test_create_part_with_add_part_payload(self):
        url = reverse('part-list')
        payload = {
            'part_number': '1234',
            'part_name': 'Oil',
            'category': 'OIL',
            'description': 'OIL',
            'stock_quantity': 150,
            'minimum_stock': 5,
            'unit_price': '50.00',
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['part_number'], payload['part_number'])
        self.assertEqual(response.data['part_name'], payload['part_name'])
        self.assertEqual(response.data['category'], payload['category'])
        self.assertEqual(response.data['description'], payload['description'])
        self.assertEqual(response.data['stock_quantity'], payload['stock_quantity'])
        self.assertEqual(response.data['minimum_stock'], payload['minimum_stock'])
        self.assertEqual(response.data['unit_price'], '50.00')
        self.assertTrue(Part.objects.filter(part_number='1234').exists())
