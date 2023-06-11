from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import CustomerDevice

from sales.serializers import CustomerDeviceSerializer

CUSTOMER_DEVICE_URL = reverse('sales:customerdevice-list')


def detail_url(device_id):
    """Return device detail url"""
    return reverse('sales:customerdevice-detail', args=[device_id])


def sample_device(user, name, vendor, price):
    """Create and return a sample device"""
    return CustomerDevice.objects.create(
        user=user,
        name=name,
        vendor=vendor,
        price=price
    )


class PublicCustomerDeviceApiTests(TestCase):
    """Test the publicly available devices"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test login is required for retrieving devices"""
        res = self.client.get(CUSTOMER_DEVICE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDevicesApiTests(TestCase):
    """Test the authorized user devices API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_devices(self):
        """Test retrieving devices"""
        CustomerDevice.objects.create(
            user=self.user,
            name='LHG5',
            vendor='Mikrotik',
            price=5000
        )
        CustomerDevice.objects.create(
            user=self.user,
            name='SXTsq',
            vendor='Mikrotik',
            price=5000
        )

        res = self.client.get(CUSTOMER_DEVICE_URL)

        customer_device = CustomerDevice.objects.all().order_by('-name')
        serializer = CustomerDeviceSerializer(customer_device, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_devices_limited_to_user(self):
        """Test that devices returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@email.com',
            'testpass'
        )
        CustomerDevice.objects.create(
            user=user2,
            name='WR840N',
            vendor='TPLink',
            price=1400
        )
        device = CustomerDevice.objects.create(
            user=self.user,
            name='WR820N',
            vendor='TPLink',
            price=900
        )

        res = self.client.get(CUSTOMER_DEVICE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], device.name)

    def test_create_device_successfull(self):
        """Test creating a new device"""
        payload = {
            'name': 'test device',
            'vendor': 'test vendor',
            'price': 1111
        }
        self.client.post(CUSTOMER_DEVICE_URL, payload)

        exists = CustomerDevice.objects.filter(
            user=self.user,
            name=payload['name'],
            vendor=payload['vendor'],
            price=payload['price']
        ).exists()
        self.assertTrue(exists)

    def test_device_invalid(self):
        """Test creating a new device with invalid payload"""
        payload = {
            'name': '',
            'vendor': '',
            'price': ''
        }
        res = self.client.post(CUSTOMER_DEVICE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_device_partial_update(self):
        """Test updating a device with PATCH"""
        device = sample_device(
            user=self.user,
            name='RB941-2nD',
            vendor='Mikrotik',
            price=2000
        )

        payload = {
            'price': 2100
        }
        url = detail_url(device.id)
        self.client.patch(url, payload)

        device.refresh_from_db()
        self.assertEqual(device.price, payload['price'])

    def test_full_update_device(self):
        """Test updating a device with PUT"""
        device = sample_device(
            user=self.user,
            name='RB941-2nD',
            vendor='Mikrotik',
            price=2000
        )
        payload = {
            'name': 'test device',
            'vendor': 'test vendor',
            'price': 1111
        }
        url = detail_url(device.id)
        self.client.put(url, payload)

        device.refresh_from_db()
        self.assertEqual(device.name, payload['name'])
        self.assertEqual(device.vendor, payload['vendor'])
        self.assertEqual(device.price, payload['price'])
