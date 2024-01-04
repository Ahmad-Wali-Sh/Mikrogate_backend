from core.models import Stage, Task

for task in Task.objects.all():
    if task.stage.name == 'Archieved':
        task.archieved = True
        task.save()

print('Update Succeful')