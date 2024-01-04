from core.models import InstallationConfirm

for confirmation in InstallationConfirm.objects.all():
    if confirmation.confirm:
        confirmation.task.installation_confirmed = True
        confirmation.task.save()

print('Update Succeful')