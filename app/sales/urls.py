from django.urls import path, include
from rest_framework.routers import DefaultRouter

from sales import views


router = DefaultRouter()
router.register('router', views.RouterViewSet)
router.register('antenna', views.AntennaViewSet)
router.register('packages', views.PackageViewSet)
# router.register('contracts', views.ContractViewSet)
router.register('log', views.LogViewSet)

router.register('contract', views.ContractsViewSet)
router.register('contract-package', views.ContractPackageViewSet)
router.register('contract-antenna', views.ContractAntennaViewSet)
router.register('contract-router', views.ContractRouterViewSet)
router.register('contract-payment', views.ContractPaymentViewSet)
router.register('contract-other-service', views.ContractOtherServiceViewSet)
router.register('contract-status', views.ContractStatusViewSet)
router.register('contract-types', views.ContractTypesViewSet)
router.register('contract-currency', views.ContractCurrencyViewSet)

app_name = 'sales'

urlpatterns = [
    path('', include(router.urls))
]
