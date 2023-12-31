from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
import django_filters
from .permissions import D7896DjangoModelPermissions
from rest_framework.decorators import authentication_classes, permission_classes

from django.db.models.signals import post_delete
from django.dispatch import receiver

from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Amendment, Contracts, Project, Tag, Stage, Task, LinkDetails,\
    CheckList, Installation, Troubleshoot, ChangeLocation,\
    OnlineSupport, TaskLog, Message, Payment, InstallationConfirm, Notification, UserNotification, User

from taskmanager import serializers

from datetime import datetime
import django_filters

import pytz
# Create your views here.


class BaseTaskManagetAttrViewSetWithUser(viewsets.GenericViewSet,
                                         mixins.ListModelMixin,
                                         mixins.CreateModelMixin):
    """Base viewset for task manager attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProjectViewSet(BaseTaskManagetAttrViewSetWithUser):
    """Manage Tasks in the database"""
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [D7896DjangoModelPermissions]

class TagViewSet(BaseTaskManagetAttrViewSetWithUser):
    """Manage Tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [D7896DjangoModelPermissions]


class StageViewSet(BaseTaskManagetAttrViewSetWithUser):
    """Manage Stages in the database"""
    queryset = Stage.objects.all()
    serializer_class = serializers.StageSerializer
    permission_classes = [D7896DjangoModelPermissions]


class TaskFilterSet(django_filters.FilterSet):
    created = django_filters.DateTimeFromToRangeFilter()
    deadline = django_filters.DateFromToRangeFilter()
    stage_net= django_filters.NumberFilter(field_name='stage', exclude=True)
    class Meta:
        model = Task
        fields = ['user','contract__contract_number', 'project', 'deadline', 'tag', 'stage','stage_net','assigned__id', 'created','contract__contract_id']



class TaskViewSet(viewsets.ModelViewSet):
    """Manage Tasks in the database"""
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = TaskFilterSet
    permission_classes = (IsAuthenticated,)
    ordering_fields = ['created', 'deadline', 'contract']
    ordering = ['created', 'deadline', 'contract']
    permission_classes = [D7896DjangoModelPermissions]

    # def get_queryset(self):
    #     contract = self.request.query_params.get('contract')
    #     if contract:
    #         return self.queryset.filter(
    #             Q(contracts__contract_number__icontains=contract)
    #         )
    #     else:
    #         return self.queryset

    def get_serializer_class(self):

        if self.action == 'list' or self.action == 'retrieve':
            return serializers.TaskDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LinkDetailsViewSet(viewsets.ModelViewSet):
    """Manage Link Details in the database"""
    queryset = LinkDetails.objects.all()
    serializer_class = serializers.LinkDetailsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, D7896DjangoModelPermissions)
    

    def get_queryset(self):

        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(task=task_id)
        else:
            return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CheckListViewSet(viewsets.ModelViewSet):
    """Manage Checklists in the database"""
    queryset = CheckList.objects.all()
    serializer_class = serializers.CheckListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, D7896DjangoModelPermissions)

    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(task=task_id)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InstallationViewSet(viewsets.ModelViewSet):
    """Manage Installations in the database"""
    queryset = Installation.objects.all()
    serializer_class = serializers.InstallationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, D7896DjangoModelPermissions)

    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(task=task_id)
        else:
            return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TroubleshootViewSet(viewsets.ModelViewSet):
    """Manage Troubleshoot in the database"""
    queryset = Troubleshoot.objects.all()
    serializer_class = serializers.TroubleshootSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, D7896DjangoModelPermissions)

    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(task=task_id)
        else:
            return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChangeLocationViewSet(viewsets.ModelViewSet):
    """Manage Change Location in the database"""
    queryset = ChangeLocation.objects.all()
    serializer_class = serializers.ChangeLocationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, D7896DjangoModelPermissions)

    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(task=task_id)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OnlineSupportViewSet(viewsets.ModelViewSet):
    """Manage Online Support in the database"""
    queryset = OnlineSupport.objects.all()
    serializer_class = serializers.OnlineSupportSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, D7896DjangoModelPermissions)

    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if self.action == 'list':
            return self.queryset.filter(task=task_id)
        return self.queryset

    def get_serializer_class(self):

        if self.action == 'retrieve':
            return serializers.OnlineSupportDetailSerializer
        user = self.request.user
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AmendmentViewSet(viewsets.GenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin):
    """Manage Amendment tasks in the database"""
    queryset = Amendment.objects.all()
    serializer_class = serializers.AmendmentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, D7896DjangoModelPermissions)

    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if self.action == 'list':
            return self.queryset.filter(task=task_id)
        return self.queryset

    def get_serializer_class(self):

        if self.action == 'list' or self.action == 'retrieve':
            return serializers.AmendmentDetailSerializer
        user = self.request.user
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskLogViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Manage Task Log in the database"""
    queryset = TaskLog.objects.all()
    serializer_class = serializers.TaskLogSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, D7896DjangoModelPermissions)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.TaskLogDetailSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(task=task_id)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Manage Message in the database"""
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,D7896DjangoModelPermissions)

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    """ Payment Clear Serializer"""
    queryset = Payment.objects.all()
    serializer_class = serializers.PaymentSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['id', 'task']
    permission_classes = (IsAuthenticated,)
    ordering_fields = ['created', 'deadline', 'contract']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,D7896DjangoModelPermissions)

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InstallationConfirmViewSet(viewsets.ModelViewSet):
    """ Installation Confirm Serializer"""
    queryset = InstallationConfirm.objects.all()
    serializer_class = serializers.InstallationConfirmSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['id', 'task']
    permission_classes = (IsAuthenticated,)
    ordering_fields = ['created', 'deadline', 'contract']
    permission_classes = (IsAuthenticated, D7896DjangoModelPermissions)


    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(id=task_id)
        else:
            return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NotificationViewSet(viewsets.ModelViewSet):
    """Manage Change Location in the database"""
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, D7896DjangoModelPermissions)

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserNotificationViewSet(viewsets.ModelViewSet):
    """Manage Change Location in the database"""
    queryset = UserNotification.objects.all().order_by('-id')
    serializer_class = serializers.UserNotificationSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['user']
    permission_classes = (IsAuthenticated, D7896DjangoModelPermissions)

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
def create_notification_all(request):
    auth_user = None
    if request.user.is_authenticated:
        auth_user = request.user
    # sender = request.data.get('sender')
    contract = request.data.get('contract')
    contractInstance = None
    if (contract):
        contractInstance = list(Contracts.objects.filter(id=contract))[0]
    content = request.data.get('content')
    task = request.data.get('task')
    taskInstance = None
    if (task):
        taskInstance = list(Task.objects.filter(id=task))[0]
    users = User.objects.exclude(pk=auth_user.id)
    notification = Notification.objects.create(sender=auth_user, content=content, task=taskInstance, contract=contractInstance)

    for user in users:
        UserNotification.objects.create(user=user, notification=notification)

    return Response({'message': 'Notification Created Successfully'})

@api_view(['POST'])
def create_notification_noc(request):
    auth_user = None
    if request.user.is_authenticated:
        auth_user = request.user
    # sender = request.data.get('sender')
    contract = request.data.get('contract')
    contractInstance = None
    if (contract):
        contractInstance = list(Contracts.objects.filter(id=contract))[0]
    content = request.data.get('content')
    task = request.data.get('task')
    taskInstance = None
    if (task):
        taskInstance = list(Task.objects.filter(id=task))[0]
    users = User.objects.filter(groups__name='NOC Stuff').exclude(pk=auth_user.id)
    notification = Notification.objects.create(sender=auth_user, content=content, task=taskInstance, contract=contractInstance)

    for user in users:
        UserNotification.objects.create(user=user, notification=notification)

    return Response({'message': 'Notification Created Successfully'})

@api_view(['POST'])
def create_notification_tech(request):
    auth_user = None
    if request.user.is_authenticated:
        auth_user = request.user
    # sender = request.data.get('sender')
    contract = request.data.get('contract')
    contractInstance = None
    if (contract):
        contractInstance = list(Contracts.objects.filter(id=contract))[0]
    content = request.data.get('content')
    task = request.data.get('task')
    taskInstance = None
    if (task):
        taskInstance = list(Task.objects.filter(id=task))[0]
    notification = Notification.objects.create(sender=auth_user, content=content, task=taskInstance, contract=contractInstance)
    users = User.objects.filter(groups__name='Technicians').exclude(pk=auth_user.id)

    for user in users:
        UserNotification.objects.create(user=user, notification=notification)

    return Response({'message': 'Notification Created Successfully'})

@api_view(['POST'])
def create_notification_l1(request):
    auth_user = None
    if request.user.is_authenticated:
        auth_user = request.user
    # sender = request.data.get('sender')
    contract = request.data.get('contract')
    contractInstance = None
    if (contract):
        contractInstance = list(Contracts.objects.filter(id=contract))[0]
    content = request.data.get('content')
    task = request.data.get('task')
    taskInstance = None
    if (task):
        taskInstance = list(Task.objects.filter(id=task))[0]
    users = User.objects.filter(groups__name='L1').exclude(pk=auth_user.id)
    notification = Notification.objects.create(sender=auth_user, content=content, task=taskInstance, contract=contractInstance)

    for user in users:
        UserNotification.objects.create(user=user, notification=notification)

    return Response({'message': 'Notification Created Successfully'})


@api_view(['POST'])
def create_notification_sales(request):
    auth_user = None
    if request.user.is_authenticated:
        auth_user = request.user
    # sender = request.data.get('sender')
    content = request.data.get('content')
    contract = request.data.get('contract')
    contractInstance = None
    if (contract):
        contractInstance = list(Contracts.objects.filter(id=contract))[0]
    task = request.data.get('task')
    taskInstance = None
    if (task):
        taskInstance = list(Task.objects.filter(id=task))[0]
    users = User.objects.filter(groups__name='Sales Stuff').exclude(pk=auth_user.id)
    notification = Notification.objects.create(sender=auth_user, content=content, task=taskInstance, contract=contractInstance)

    for user in users:
        UserNotification.objects.create(user=user, notification=notification)

    return Response({'message': 'Notification Created Successfully'})


# @api_view(['POST'])
# def create_notification_users(request):
#     auth_user = None
#     if request.user.is_authenticated:
#         auth_user = request.user
#     # sender = request.data.get('sender')
#     contract = request.data.get('contract')
#     contractInstance = None
#     if (contract):
#         contractInstance = list(Contracts.objects.filter(id=contract))[0]
#     content = request.data.get('content')
#     user_ids = request.data.get('user_ids')
#     numbers_list = [int(num) for num in user_ids.split(',')]
#     print(user_ids)
#     task = request.data.get('task')
#     taskInstance = None
#     if (task):
#         taskInstance = list(Task.objects.filter(id=task))[0]
#     users = User.objects.filter(id__in=numbers_list).exclude(pk=auth_user.id)
#     notification = Notification.objects.create(sender=auth_user, content=content, task=taskInstance, contract=contractInstance)

#     for user in users:
#         UserNotification.objects.create(user=user, notification=notification)

#     return Response({'message': 'Notification Created Successfully'})


@api_view(['POST'])
def create_notification_users(request):
    auth_user = None
    if request.user.is_authenticated:
        auth_user = request.user

    contract = request.data.get('contract')
    contract_instance = None
    if contract:
        contract_instance = Contracts.objects.filter(id=contract).first()

    content = request.data.get('content')
    user_ids = request.data.get('user_ids')

    if user_ids:
        numbers_list = [int(num) for num in user_ids.split(',')]
    else:
        numbers_list = []

    task = request.data.get('task')
    task_instance = None
    if task:
        task_instance = Task.objects.filter(id=task).first()

    users = User.objects.filter(id__in=numbers_list).exclude(pk=auth_user.id)

    notification = Notification.objects.create(sender=auth_user, content=content, task=task_instance, contract=contract_instance)

    for user in users:
        UserNotification.objects.create(user=user, notification=notification)

    return Response({'message': 'Notification Created Successfully'})


class ModelCountsView(viewsets.ViewSet):
    def list(self, request):
        cpe_count = Task.objects.filter(project__name='CPE').exclude(stage__name='Archieved').count()
        amendment_count = Task.objects.filter(project__name='Amendment').exclude(stage__name='Archieved').count()
        online_support_count = Task.objects.filter(project__name='Online Support').exclude(stage__name='Archieved').count()
        troubleshoot_count = Task.objects.filter(project__name='Troubleshoot').exclude(stage__name='Archieved').count() 

        data = {
            'cpe_count': cpe_count,
            'amendment_count': amendment_count,
            'online_support_count': online_support_count,
            'troubleshoot_count': troubleshoot_count,
        }

        serializer = serializers.ModelsCountSerializer(data)

        return Response(serializer.data)
