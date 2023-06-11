from django.urls import path, include
from rest_framework.routers import DefaultRouter

from taskmanager import views


router = DefaultRouter()
# router.register('project', views.ProjectViewSet)
# router.register('tag', views.TaskManagerTagsViewSet)
# router.register('label', views.TaskManagerLabelsViewSet)
# router.register('task', views.TaskManagerViewSet)
router.register('project', views.ProjectViewSet)
router.register('tag', views.TagViewSet)
router.register('stage', views.StageViewSet)
router.register('task', views.TaskViewSet)
router.register('linkDetails', views.LinkDetailsViewSet)
router.register('checklist', views.CheckListViewSet)
router.register('installation', views.InstallationViewSet)
router.register('troubleshoot', views.TroubleshootViewSet)
router.register('changeLocation', views.ChangeLocationViewSet)
router.register('onlineSupport', views.OnlineSupportViewSet)
router.register('amendment', views.AmendmentViewSet)
router.register('taskLog', views.TaskLogViewSet)
router.register('message', views.MessageViewSet)

app_name = 'taskmanager'

urlpatterns = [
  path('', include(router.urls))
]