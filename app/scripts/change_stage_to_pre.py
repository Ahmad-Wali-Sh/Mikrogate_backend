import json
from core.models import Task, Stage

def get_latest_stage_change(task):
    history_entries = task.changes.filter(changes__contains='"stage"').order_by('-timestamp')

    if history_entries.exists():
        return history_entries.first()

    return None

def update_task_to_previous_stage(task):
    latest_stage_change = get_latest_stage_change(task)

    if latest_stage_change:
        try:
            changes_data = json.loads(latest_stage_change.changes)
            previous_stage_name = changes_data['stage'][0]

            if previous_stage_name != 'Archieved':   
                previous_stage = Stage.objects.get(name=previous_stage_name)
                task.stage = previous_stage
                task.save()
        except (json.JSONDecodeError, IndexError, KeyError, Stage.DoesNotExist):
            pass

archived_tasks = Task.objects.filter(stage__name='Archieved')

for task in archived_tasks:
    update_task_to_previous_stage(task)

print('Job is Done Succesfully!')