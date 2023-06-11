from rest_framework import serializers

from core.models import ContractAntenna, ContractCurrency, ContractOtherService, ContractPackage, ContractPayment, ContractRouter, ContractStatus, ContractTypes, Contracts, Router, Antenna, Package, Log

from user.serializers import UserSerializer

class RouterSerializer(serializers.ModelSerializer):
    """Serializer for cutomer device objects"""

    class Meta:
        model = Router
        fields = ('id', 'name', 'price', 'available', 'updated', 'created')
        read_only_fields = ('id',)


class AntennaSerializer(serializers.ModelSerializer):
    """Serializer for cutomer device objects"""

    class Meta:
        model = Antenna
        fields = ('id', 'name', 'price', 'available', 'updated', 'created')
        read_only_fields = ('id',)


class PackageSerializer(serializers.ModelSerializer):
    """Serializer for package objects"""

    class Meta:
        model = Package
        fields = ('id', 'name', 'type', 'price',
                  'available', 'updated', 'created')
        read_only_fields = ('id',)


class LogSerializer(serializers.ModelSerializer):
    """Serializer for log objects"""

    class Meta:
        model = Log
        fields = ('id', 'user', 'contract', 'log', 'updated')
        read_only_fields = ('id',)


class ContractStatusSerializer(serializers.ModelSerializer):
    """Serializer for contract status objects"""
    class Meta:
        model = ContractStatus
        fields = (
            'id',
            'name',
        )
        read_only_fields = ('id',)


class ContractTypesSerializer(serializers.ModelSerializer):
    """Serializer for contract-type objects"""
    class Meta:
        model = ContractTypes
        fields = (
            'id',
            'name',
        )
        read_only_fields = ('id',)


class ContractCurrencySerializer(serializers.ModelSerializer):
    """serializer for contract currency objects"""
    class Meta:
        model = ContractCurrency
        fields = (
            'id',
            'name',
        )
        read_only_fields = ('id',)


class ContractsSerializer(serializers.ModelSerializer):
    """Serialzier for contracts objects"""

    status = serializers.PrimaryKeyRelatedField(
        queryset=ContractStatus.objects.all())
    contract_type = serializers.PrimaryKeyRelatedField(
        queryset=ContractTypes.objects.all())

    class Meta:
        model = Contracts
        fields = ('id',
                  'user',
                  'contract_number',
                  'contract_id',
                  'contract_type',
                  'name',
                  'contact',
                  'referral',
                  'organization',
                  'email',
                  'address',
                  'date',
                  'activation',
                  'valid',
                  'status',
                  'note',)
        read_only_fields = ('id', 'user',)


class ContractsDetailSerializer(ContractsSerializer):
    user = UserSerializer(read_only=True)
    status = ContractStatusSerializer(read_only=True)
    contract_type = ContractTypesSerializer(read_only=True)


class ContractPackageSerialzier(serializers.ModelSerializer):
    """Serializer for contract package objects"""
    contract = serializers.PrimaryKeyRelatedField(
        queryset=Contracts.objects.all()
    )
    package = serializers.PrimaryKeyRelatedField(
        queryset=Package.objects.all()
    )
    class Meta:
        model = ContractPackage
        fields = (
            'id',
            'contract',
            'package',
            'price',
        )
        read_only_fields = ('id',)


class ContractPackageDetailSerializer(ContractPackageSerialzier):
    """Serializer for contract detials"""
    package = PackageSerializer(read_only=True)


class ContractAntennaSerializer(serializers.ModelSerializer):
    """serialzier for contract antenna objects"""
    contract = serializers.PrimaryKeyRelatedField(
        queryset = Contracts.objects.all()
    )
    antenna = serializers.PrimaryKeyRelatedField(
        queryset=Antenna.objects.all()
    )
    class Meta:
        model = ContractAntenna
        fields = (
            'id',
            'contract',
            'antenna',
            'condition',
            'serial_number',
            'quantity',
            'amount',
            'Lease_amount',
            'total_amount',
            'collected',
        )
        read_only_fields = ('id',)


class ContractAntennaDetailSerializer(ContractAntennaSerializer):
    """serializer for contract antenna detail"""
    antenna = AntennaSerializer(read_only=True)


class ContractRouterSerializer(serializers.ModelSerializer):
    """serializer for contract router objects"""
    contract = serializers.PrimaryKeyRelatedField(
        queryset = Contracts.objects.all()
    )
    router = serializers.PrimaryKeyRelatedField(
        queryset=Router.objects.all()
    )
    class Meta:
        model = ContractRouter
        fields = (
            'id',
            'contract',
            'router',
            'condition',
            'serial_number',
            'quantity',
            'amount',
            'Lease_amount',
            'total_amount',
            'collected',
        )
        read_only_fields = ('id',)


class ContractRouterDetailSerializer(ContractRouterSerializer):
    """serializer for contract router detail"""
    router = RouterSerializer(read_only=True)


class ContractPaymentSerializer(serializers.ModelSerializer):
    """Serializer for contract payment objects"""
    contract = serializers.PrimaryKeyRelatedField(
        queryset=Contracts.objects.all()
    )
    currency = serializers.PrimaryKeyRelatedField(
        queryset=ContractCurrency.objects.all()
    )
    class Meta:
        model = ContractPayment
        fields = (
            'id',
            'contract',
            'payment_total',
            'service_charge',
            'other_charges',
            'discount',
            'lease_deposit',
            'grand_total',
            'currency',
        )
        read_only_fields = ('id',)


class ContractPaymentDetailSerializer(ContractPaymentSerializer):
    currency = ContractCurrencySerializer(read_only=True)


class ContractOtherServiceSerializer(serializers.ModelSerializer):
    """Serializer for contract other service objects"""
    contract = serializers.PrimaryKeyRelatedField(
        queryset=Contracts.objects.all()
    )
    class Meta:
        model = ContractOtherService
        fields = ('id', 'contract', 'service_type', 'description', 'payment_method', 'price')
        read_only_fields = ('id',)
