from rest_framework import serializers
from core.models import Amendment, Message, OnlineSupport, Project,\
     Tag, Stage, Task, LinkDetails, CheckList, Installation,\
     TaskLog, Troubleshoot, ChangeLocation, Contracts, User, Payment, InstallationConfirm, ContractPackage, ContractAntenna, ContractRouter

from user.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Task's Project"""

    class Meta:
        model = Project
        fields = ('id', 'name')
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    """Serialzier for Task's Tag"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class StageSerializer(serializers.ModelSerializer):
    """Serialzier for Task's Stage"""

    class Meta:
        model = Stage
        fields = ('id', 'name')
        read_only_fields = ('id',)

class TaskContractSerializer(serializers.ModelSerializer):
    """Serializer for the task contract"""
    package = serializers.SerializerMethodField()
    antenna = serializers.SerializerMethodField()
    router = serializers.SerializerMethodField()

    def get_package(self, obj):
        print(obj.id)
        pack = ContractPackage.objects.filter(contract=obj.id).values('package__name', 'price')
        if (pack):
            return pack[0]
        else: return ''
    def get_antenna(self, obj):
        print(obj.id)
        pack = ContractAntenna.objects.filter(contract=obj.id).values('antenna__name')
        if (pack):
            return pack[0]
        else: return ''
    def get_router(self, obj):
        print(obj.id)
        pack = ContractRouter.objects.filter(contract=obj.id).values('router__name')
        if (pack):
            return pack[0]
        else: return ''
    class Meta:
        model = Contracts
        fields = ('id', 'contract_number', 'contract_id', 'organization', 'name', 'contact', 'address', 'package', 'antenna','router')
        read_only_fields = ('id',)

class ChangeHistoryField(serializers.ListField):
    childs = serializers.JSONField()

    def to_representation(self, data):
        return super().to_representation(data.values('id', 'changes', 'timestamp', 'action', 'actor_id'))


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task-Manager's Task"""

    contract = serializers.PrimaryKeyRelatedField(
        queryset=Contracts.objects.all()
    )
    # contract = TaskContractSerializer()
    # project = ProjectSerializer(instance='name')
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all()
    )
    tag = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all()
    )
    # tag = TagSerializer()
    # stage = StageSerializer()
    stage = serializers.PrimaryKeyRelatedField(
        queryset=Stage.objects.all()
    )
    # assigned = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=User.objects.all()
    # )
    assigned = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )

    changes = ChangeHistoryField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'contract', 'project',
                  'tag', 'deadline', 'stage', 'assigned', 'description', 'created', 'changes' )
        read_only_fields = ('id', 'user',)


class TaskDetailSerializer(TaskSerializer):
    """Serialize a task detail"""
    user = UserSerializer(read_only=True)
    contract = TaskContractSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    tag = TagSerializer(read_only=True)
    stage = StageSerializer(read_only=True)
    assigned = UserSerializer(read_only=True, many=True)


class LinkDetailsSerializer(serializers.ModelSerializer):
    """Serializer for Task's link details"""
    user = UserSerializer(read_only=True)
    class Meta:
        model = LinkDetails
        fields = ('id', 'task', 'installation_type', 'device', 'access_point', 'signal', 'ccq', 'cable',
                  'connector', 'payment', 'bill_number', 'installation_date', 'additional_details', 'user')
    read_only_fields = ('id','user')


class CheckListSerializer(serializers.ModelSerializer):
    """Serialzier for Task's checklist"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = CheckList
        fields = ('id', 'task', 'cable', 'stand', 'router',
                  'antenna', 'router_os', 'signal', 'dns', 'user')
        read_only_fields = ('id','user')


class InstallationSerializer(serializers.ModelSerializer):
    """Serialzier for Installation Tasks"""
    user = UserSerializer(read_only=True)
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )

    class Meta:
        model = Installation
        fields = ('id', 'task', 'description', 'pppoe_user',
                  'pppoe_password', 'user')
        read_only_fields = ('id','user')



class TroubleshootSerializer(serializers.ModelSerializer):
    """Serialzier for Troubleshoot Tasks"""
    user = UserSerializer(read_only=True)
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )

    class Meta:
        model = Troubleshoot
        fields = ('id', 'task', 'address', 'contact', 'problem',
                  'service_charge', 'description', 'user')
        read_only_fields = ('id','user')


class ChangeLocationSerializer(serializers.ModelSerializer):
    """Serialzier for Change Location Tasks"""
    user = UserSerializer(read_only=True)
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )

    class Meta:
        model = ChangeLocation
        fields = ('id', 'task', 'address', 'contact', 'service_charge', 'description', 'user')
        read_only_fields = ('id','user')


class OnlineSupportSerializer(serializers.ModelSerializer):
    """Serializer for Online Support Tasks"""
    user = UserSerializer(read_only=True)
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )

    class Meta:
        model = OnlineSupport
        fields = ('id', 'task', 'contact', 'by', 'description', 'user')
        read_only_fields = ('id','user')


class OnlineSupportDetailSerializer(OnlineSupportSerializer):
    task = TaskSerializer(read_only=True)


class AmendmentSerializer(serializers.ModelSerializer):
    """Serializer for amendment tasks"""
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Amendment
        fields = ('id', 'task', 'user', 'message', 'created', 'user')
        read_only_fields = ('id','user')


class AmendmentDetailSerializer(AmendmentSerializer):
    task = TaskSerializer(read_only=True)
    user = UserSerializer(read_only=True)


class TaskLogSerializer(serializers.ModelSerializer):
    """Serializer for Task's Log Note"""

    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )

    class Meta:
        model = TaskLog
        fields = ('id', 'user', 'task', 'body', 'created')
        read_only_fields = ('id','user',)


class TaskLogDetailSerializer(TaskLogSerializer):
    user = UserSerializer(read_only=True)


class MessageSerializer(serializers.ModelSerializer):
    """Serialzier for Task's Messages"""

    task = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all()
    )
    to = serializers.PrimaryKeyRelatedField(
        many=True,
    queryset=User.objects.all()
    )

    class Meta:
        model = Message
        fields = ('id', 'user', 'task', 'to', 'body', 'created')
        read_only_fields = ('id',)


class PaymentSerializer(serializers.ModelSerializer):
    """" Serializer for Payment Clear"""
    user = UserSerializer(read_only=True)
    class Meta: 
        model = Payment
        fields = ('id', 'task', 'payment', 'updated', 'created', 'user')
        read_only_fields = ('id','user')

class InstallationConfirmSerializer(serializers.ModelSerializer):
    """ Serializer for InstallationConfirm"""
    user = UserSerializer(read_only=True)
    class Meta: 
        model = InstallationConfirm
        fields = ('id', 'task', 'confirm', 'updated', 'created', 'user')
        read_only_fields = ('id', 'user')