from atexit import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models

from import_export.admin import ImportExportModelAdmin


class UserAdmin(BaseUserAdmin):
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
admin.site.register(models.Router)
admin.site.register(models.Antenna)

@admin.register(models.Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'available', 'type', 'price')

admin.site.register(models.Log)
admin.site.register(models.Project)
admin.site.register(models.Tag)
admin.site.register(models.Task)
admin.site.register(models.Stage)
admin.site.register(models.Installation)
admin.site.register(models.Troubleshoot)
admin.site.register(models.OnlineSupport)
admin.site.register(models.ChangeLocation)
admin.site.register(models.CheckList)
admin.site.register(models.LinkDetails)
admin.site.register(models.TaskLog)
admin.site.register(models.Message)
@admin.register(models.Contracts)
class ContractAdmin(ImportExportModelAdmin):
    pass
admin.site.register(models.ContractPackage)
admin.site.register(models.ContractAntenna)
admin.site.register(models.ContractRouter)
admin.site.register(models.ContractPayment)
admin.site.register(models.ContractTypes)
admin.site.register(models.ContractCurrency)
admin.site.register(models.ContractStatus)

admin.site.register(models.Payment)
admin.site.register(models.InstallationConfirm)