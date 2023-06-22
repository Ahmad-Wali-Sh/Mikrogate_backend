from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
import django_filters

from django.db.models import Q

from core.models import Amendment, Contracts, Project, Tag, Stage, Task, LinkDetails,\
    CheckList, Installation, Troubleshoot, ChangeLocation,\
    OnlineSupport, TaskLog, Message, Payment, InstallationConfirm

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


class TagViewSet(BaseTaskManagetAttrViewSetWithUser):
    """Manage Tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class StageViewSet(BaseTaskManagetAttrViewSetWithUser):
    """Manage Stages in the database"""
    queryset = Stage.objects.all()
    serializer_class = serializers.StageSerializer


class TaskFilterSet(django_filters.FilterSet):
    created = django_filters.DateTimeFromToRangeFilter()
    deadline = django_filters.DateFromToRangeFilter()
    class Meta:
        model = Task
        fields = ['user','contract__contract_number', 'project', 'deadline', 'tag', 'stage','assigned__id', 'created','contract__contract_id']



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
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(task=task_id)
        else:
            return self.queryset

    def perform_create(self, serializer):
        serializer.save()


class CheckListViewSet(viewsets.ModelViewSet):
    """Manage Checklists in the database"""
    queryset = CheckList.objects.all()
    serializer_class = serializers.CheckListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(task=task_id)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save()


class InstallationViewSet(viewsets.ModelViewSet):
    """Manage Installations in the database"""
    queryset = Installation.objects.all()
    serializer_class = serializers.InstallationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(task=task_id)
        else:
            return self.queryset

    def perform_create(self, serializer):
        serializer.save()


class TroubleshootViewSet(viewsets.ModelViewSet):
    """Manage Troubleshoot in the database"""
    queryset = Troubleshoot.objects.all()
    serializer_class = serializers.TroubleshootSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(task=task_id)
        else:
            return self.queryset

    def perform_create(self, serializer):
        serializer.save()


class ChangeLocationViewSet(viewsets.ModelViewSet):
    """Manage Change Location in the database"""
    queryset = ChangeLocation.objects.all()
    serializer_class = serializers.ChangeLocationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        task_id = self.request.query_params.get('id')
        if task_id:
            return self.queryset.filter(task=task_id)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save()


class OnlineSupportViewSet(viewsets.ModelViewSet):
    """Manage Online Support in the database"""
    queryset = OnlineSupport.objects.all()
    serializer_class = serializers.OnlineSupportSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
        serializer.save()


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
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """ Payment Clear Serializer"""
    queryset = Payment.objects.all()
    serializer_class = serializers.PaymentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InstallationConfirmViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """ Installation Confirm Serializer"""
    queryset = InstallationConfirm.objects.all()
    serializer_class = serializers.InstallationConfirmSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)