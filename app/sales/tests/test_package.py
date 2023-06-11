from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Package

from sales.serializers import PackageSerializer

PACKAGE_URL = reverse('sales:package-list')


class PublicPackagesApiTests(TestCase):
    """Test the publicly available packages API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving packages"""
        res = self.client.get(PACKAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePackageApiTests(TestCase):
    """Test the authorized user packages API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_packages(self):
        """Test retrieving packages"""
        Package.objects.create(
            user=self.user,
            name='70GB',
            type='Limited',
            price=1400.00
        )
        Package.objects.create(
            user=self.user,
            name='1Mb',
            type='Unlimited',
            price=4000.00
        )

        res = self.client.get(PACKAGE_URL)

        packages = Package.objects.all().order_by('-name')
        serializer = PackageSerializer(packages, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_packages_limited_to_user(self):
        """Test that packages returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@email.com',
            'testpass'
        )
        Package.objects.create(
            user=user2,
            name='100GB',
            type='Limited',
            price=2750.00
        )
        package = Package.objects.create(
            user=self.user,
            name='200GB',
            type='Limited',
            price=6600.0
        )
        res = self.client.get(PACKAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], package.name)
        self.assertEqual(res.data[0]['type'], package.type)
        self.assertEqual(res.data[0]['price'], package.price)

    def test_create_package_successfull(self):
        """Test creating a new package is successfull"""
        payload = {
            'name': '2Mb-24-hr',
            'type': 'Unlimited',
            'price': 7500
        }
        self.client.post(PACKAGE_URL, payload)

        exists = Package.objects.filter(
            user=self.user,
            name=payload['name'],
            type=payload['type'],
            price=payload['price']
        ).exists()
        self.assertTrue(exists)

    def test_create_package_invalid(self):
        """Test creating package with invalid payload"""
        payload = {
            'name': '',
            'type': '',
            'price': ''
        }
        res = self.client.post(PACKAGE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
