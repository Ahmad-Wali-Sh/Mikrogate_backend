from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
import django_filters
import rest_framework_filters as restfilters

from django.db.models import Q

# from rest_flex_fields import FlexFieldsModelViewSet

from core.models import ContractAntenna, ContractCurrency, ContractOtherService, ContractPackage, ContractPayment, ContractRouter, ContractStatus, ContractTypes, Contracts, Router, Antenna, Package, Log

from sales import serializers

import pytz

from datetime import datetime


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BaseSaleAttrViewSet(viewsets.ModelViewSet):
    """Base viewset for user owned sales attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for current authenticated user only"""
        return self.queryset.all().order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class RouterViewSet(BaseSaleAttrViewSet):
    """Manage devices in the database"""
    queryset = Router.objects.all()
    serializer_class = serializers.RouterSerializer


class AntennaViewSet(BaseSaleAttrViewSet):
    """Manage devices in the database"""
    queryset = Antenna.objects.all()
    serializer_class = serializers.AntennaSerializer


class PackageViewSet(BaseSaleAttrViewSet):
    """Manage packages in the database"""
    queryset = Package.objects.all()
    serializer_class = serializers.PackageSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        available = self.request.query_params.get('available')
        if available:
            return self.queryset.filter(available=True)
        else:
            return self.queryset


class LogViewSet(viewsets.ModelViewSet):
    """Manage logs in the database"""
    queryset = Log.objects.all()
    serializer_class = serializers.LogSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for current authenticated user only"""

        contract_no = self.request.query_params.get('contract-no')

        queryset = self.queryset

        if contract_no:
            return queryset.filter(contract__icontains=contract_no).order_by('-updated')
        else:
            return queryset.all().order_by('-updated')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)

    


class ContractFilterSet(django_filters.FilterSet):
    date = django_filters.DateTimeFromToRangeFilter()
    class Meta:
        model = Contracts
        fields = ['user','contract_number', 'contract_id', 'date', 'activation', 'valid','status', 'contract_type', 'contractpackage__package', 'contractrouter__router', 'contractantenna__antenna']

class ContractsViewSet(viewsets.ModelViewSet):
    """Manage contracts in the database"""
    queryset = Contracts.objects.all()
    serializer_class = serializers.ContractsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ContractFilterSet
    ordering_fields = ['contract_number', 'date',]
    ordering = ['date', 'contract_number']

    def get_serializer_class(self):
        """Return apropriate serializer class"""
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.ContractsDetailSerializer
        return self.serializer_class
    
    def get_queryset(self):
        query = self.request.query_params.get('query')
        status = self.request.query_params.get('contract-status')
        created_by = self.request.query_params.get('created_by')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        queryset = self.queryset

        if start_date:
            # parsed_date1 = datetime.strptime(start_date, '%Y-%m-%d')
            # kabul_timezone = pytz.timezone('Asia/Kabul')
            # date_search1 = kabul_timezone.localize(parsed_date1)
            # parsed_date2 = datetime.strptime(end_date, '%Y-%m-%d')
            # date_search2 = kabul_timezone.localize(parsed_date2)
            return queryset.filter(date__gte=start_date, date__lte=end_date)

        if created_by:
            return queryset.filter(user=created_by)
        if query:
            return queryset.filter(
                Q(contract_number__icontains=query) |
                Q(contact__icontains=query) |
                Q(contract_id__icontains=query) |
                Q(name__icontains=query)
            )
        if status:
            return queryset.filter(status=status)
        # else:
            # bandwidth = Package.objects.all()
            # return self.queryset.filter(
            #     Q(contracts__contract_number__icontains=contract)
            # )
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContractPackageViewSet(viewsets.ModelViewSet):
    """Manage contract package in the database"""
    queryset = ContractPackage.objects.all()
    serializer_class = serializers.ContractPackageSerialzier
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.ContractPackageDetailSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        contract = self.request.query_params.get('contract')
        if contract:
            return queryset.filter(contract=contract)
        else:
            return self.queryset


class ContractAntennaViewSet(viewsets.ModelViewSet):
    """Manage contract antenna on the database"""
    queryset = ContractAntenna.objects.all()
    serializer_class = serializers.ContractAntennaSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """return apropriate serializer class"""
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.ContractAntennaDetailSerializer
        else:
            return self.serializer_class
    
    def get_queryset(self):
        queryset = self.queryset
        contract = self.request.query_params.get('contract')
        if contract:
            return queryset.filter(contract=contract)
        else:
            return self.queryset


class ContractRouterViewSet(viewsets.ModelViewSet):
    """Manage contract router in the database"""
    queryset = ContractRouter.objects.all()
    serializer_class = serializers.ContractRouterSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """return apropriate serializer class"""
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.ContractRouterDetailSerializer
        else:
            return self.serializer_class
    
    def get_queryset(self):
        queryset = self.queryset
        contract = self.request.query_params.get('contract')
        if contract:
            return queryset.filter(contract=contract)
        else:
            return self.queryset


class ContractPaymentViewSet(viewsets.ModelViewSet):
    """Manage contract payment in the database"""
    queryset = ContractPayment.objects.all()
    serializer_class = serializers.ContractPaymentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """return aproporiate serializer class"""
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.ContractPaymentDetailSerializer
        else:
            return self.serializer_class
    
    def get_queryset(self):
        queryset = self.queryset
        contract = self.request.query_params.get('contract')
        if contract:
            return queryset.filter(contract=contract)
        else:
            return self.queryset


class ContractOtherServiceViewSet(viewsets.GenericViewSet,
                                  mixins.CreateModelMixin,
                                  mixins.ListModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin):
    """Manage contract other service in the database"""
    queryset = ContractOtherService.objects.all()
    serializer_class = serializers.ContractOtherServiceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        contract = self.request.query_params.get('contract')
        if contract:
            return queryset.filter(contract=contract)
        else:
            return self.queryset


class ContractCurrencyViewSet(viewsets.GenericViewSet,
                              mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin):
    """Manage contract payment currencies in the database"""
    queryset = ContractCurrency.objects.all()
    serializer_class = serializers.ContractCurrencySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ContractStatusViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Manage contract status in the database"""
    queryset = ContractStatus.objects.all()
    serializer_class = serializers.ContractStatusSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class ContractTypesViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
    """Manage contract types in the database"""
    queryset = ContractTypes.objects.all()
    serializer_class = serializers.ContractTypesSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

