from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Contract, CustomerDevice, Package

from sales.serializers import ContractSerializer

CONTRACT_URL = reverse('sales:contract-list')


def detail_url(contract_id):
    """Return contract detail url"""
    return reverse('sales:contract-detail', args=[contract_id])


def sample_device(user, name, vendor, price):
    """Create and return a sample device"""
    return CustomerDevice.objects.create(
        user=user,
        name=name,
        vendor=vendor,
        price=price
    )


def sample_package(user, name, type, price):
    """Create and return a sample package"""
    return Package.objects.create(
        user=user,
        name=name,
        type=type,
        price=price
    )


def sample_contract(user, **params):
    """Create and return a sample contracr"""
    defaults = {
        'contract_no': '200404-1256',
        'poc_name': 'Basir Ahmad Nasrat',
        'poc_number': '0799404727',
        'address': 'Farqa',
        'other_charges': 500,
        'service_charge': 500,
        'grand_total': 3500
    }
    defaults.update(params)

    return Contract.objects.create(user=user, **defaults)


class PublicContractApiTest(TestCase):
    """Test unauthenticated API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(CONTRACT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateContractApiTest(TestCase):
    """Test authenticated API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'password123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_contracts(self):
        """Test retrieving a list of contracts"""
        sample_contract(user=self.user)
        sample_contract(user=self.user)

        res = self.client.get(CONTRACT_URL)

        contracts = Contract.objects.all().order_by('-id')
        serializer = ContractSerializer(contracts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_contracts_limited_to_user(self):
        """Test retrieving contracts for user"""
        user2 = get_user_model().objects.create_user(
            'other@email.com',
            'testpass'
        )
        sample_contract(user=user2)
        sample_contract(user=self.user)

        res = self.client.get(CONTRACT_URL)

        contracts = Contract.objects.filter(user=self.user)
        serializer = ContractSerializer(contracts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_contract_detail(self):
        """Test viewing a contract details"""
        contract = sample_contract(user=self.user)
        contract.packages.add(sample_package(
            user=self.user,
            name='1Mb-24-hr',
            type='Unlimitied',
            price=4000
        ))
        contract.customerDevices.add(sample_device(
            user=self.user,
            name='SXT-lite5',
            vendor='mikrotik',
            price=4000
        ))

        url = detail_url(contract.id)
        res = self.client.get(url)

        serializer = ContractSerializer(contract)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_contract(self):
        """Test creating contract"""
        payload = {
            'contract_no': '200404-1256',
            'poc_name': 'Basir Ahmad Nasrat',
            'poc_number': '0799404727',
            'address': 'Farqa',
            'other_charges': 500,
            'service_charge': 500,
            'grand_total': 3500
        }
        res = self.client.post(CONTRACT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        contract = Contract.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(contract, key))

    def test_create_contract_with_package(self):
        """Test create contract with package"""
        package1 = sample_package(
            user=self.user,
            name='1Mb-24-hr',
            type='Unlimitied',
            price=4000
        )
        payload = {
            'contract_no': '200404-1256',
            'poc_name': 'Basir Ahmad Nasrat',
            'poc_number': '0799404727',
            'address': 'Farqa',
            'packages': package1.id,
            'other_charges': 500,
            'service_charge': 500,
            'grand_total': 3500
        }
        res = self.client.post(CONTRACT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        contract = Contract.objects.get(id=res.data['id'])
        packages = contract.packages.all()
        self.assertEqual(packages.count(), 1)
        self.assertIn(package1, packages)

    def test_create_contract_with_device(self):
        """Test create contract with device"""
        device1 = sample_device(
            user=self.user,
            name='SXT-lite5',
            vendor='mikrotik',
            price=4000
        )
        payload = {
            'contract_no': '200404-1256',
            'poc_name': 'Basir Ahmad Nasrat',
            'poc_number': '0799404727',
            'address': 'Farqa',
            'customerDevices': device1.id,
            'other_charges': 500,
            'service_charge': 500,
            'grand_total': 3500
        }
        res = self.client.post(CONTRACT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        contract = Contract.objects.get(id=res.data['id'])
        devices = contract.customerDevices.all()
        self.assertEqual(devices.count(), 1)
        self.assertIn(device1, devices)

    def test_contract_partial_update(self):
        """Test updating a contract with PATCH"""
        contract = sample_contract(user=self.user)
        contract.packages.add(sample_package(
            user=self.user,
            name='2Mb-24-hr',
            type='Unlimitied',
            price=7000
        ))
        new_package = sample_package(
            user=self.user,
            name='3Mb-24-hr',
            type='Unlimitied',
            price=11000
        )

        payload = {
            'address': '64-Metre',
            'packages': [new_package.id]
        }
        url = detail_url(contract.id)
        self.client.patch(url, payload)

        contract.refresh_from_db()
        self.assertEqual(contract.address, payload['address'])
        package = contract.packages.all()
        self.assertEqual(len(package), 1)
        self.assertIn(new_package, package)

    def test_full_update_contract(self):
        """Test updating a contract with PUT"""
        contract = sample_contract(user=self.user)
        contract.packages.add(sample_package(
            user=self.user,
            name='2Mb-24-hr',
            type='Unlimited',
            price=8000
        ))
        payload = {
            'contract_no': '200404-1256',
            'poc_name': 'Basir Ahmad Nasrat',
            'poc_number': '0799404727',
            'address': 'Qol-Urdu',
            'other_charges': 500,
            'service_charge': 500,
            'grand_total': 3500
        }
        url = detail_url(contract.id)
        self.client.put(url, payload)

        contract.refresh_from_db()
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(contract, key))
        packages = contract.packages.all()
        self.assertEqual(len(packages), 0)
