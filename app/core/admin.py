from atexit import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .resources import ContractResources

from core import models

from import_export.admin import ImportExportModelAdmin


class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'avatar')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Router, ImportExportModelAdmin)
admin.site.register(models.Antenna, ImportExportModelAdmin)
admin.site.register(models.Log, ImportExportModelAdmin)
admin.site.register(models.Project, ImportExportModelAdmin)
admin.site.register(models.Tag, ImportExportModelAdmin)
admin.site.register(models.Task, ImportExportModelAdmin)
admin.site.register(models.Stage, ImportExportModelAdmin)
admin.site.register(models.Installation, ImportExportModelAdmin)
admin.site.register(models.Troubleshoot, ImportExportModelAdmin)
admin.site.register(models.OnlineSupport, ImportExportModelAdmin)
admin.site.register(models.ChangeLocation, ImportExportModelAdmin)
admin.site.register(models.CheckList, ImportExportModelAdmin)
admin.site.register(models.LinkDetails, ImportExportModelAdmin)
admin.site.register(models.TaskLog, ImportExportModelAdmin)
admin.site.register(models.Message, ImportExportModelAdmin)
# admin.site.register(models.Contracts, ImportExportModelAdmin)
admin.site.register(models.ContractPackage, ImportExportModelAdmin)
admin.site.register(models.ContractAntenna, ImportExportModelAdmin)
admin.site.register(models.ContractRouter, ImportExportModelAdmin)
admin.site.register(models.ContractPayment, ImportExportModelAdmin)
admin.site.register(models.ContractTypes, ImportExportModelAdmin)
admin.site.register(models.ContractCurrency, ImportExportModelAdmin)
admin.site.register(models.ContractStatus, ImportExportModelAdmin)
admin.site.register(models.Payment, ImportExportModelAdmin)
admin.site.register(models.Amendment, ImportExportModelAdmin)
admin.site.register(models.InstallationConfirm, ImportExportModelAdmin)

@admin.register(models.Package)
class PackageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'available', 'type', 'price')


@admin.register(models.Contracts)
class ContractAdmin(ImportExportModelAdmin):
    resource_class = ContractResources