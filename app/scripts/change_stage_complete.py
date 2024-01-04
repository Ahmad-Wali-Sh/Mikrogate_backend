from core.models import Task

for task in Task.objects.all():
    if task.stage.name == 'Archieved':
        task.stage.name == 'Completed'
        task.save()

print('Update Succeful')