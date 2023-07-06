from rest_framework import serializers
from core.models import Amendment, Message, OnlineSupport, Project,\
     Tag, Stage, Task, LinkDetails, CheckList, Installation,\
     TaskLog, Troubleshoot, ChangeLocation, Contracts, User, Payment, InstallationConfirm

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

    class Meta:
        model = Contracts
        fields = ('id', 'contract_number', 'contract_id', 'organization', 'name', 'contact', 'address',)
        read_only_fields = ('id',)


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

    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'contract', 'project',
                  'tag', 'deadline', 'stage', 'assigned', 'description' )
        read_only_fields = ('id', 'user',)


class TaskDetailSerializer(TaskSerializer):
    """Serialize a task detail"""
    # user = UserSerializer(read_only=True)
    contract = TaskContractSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    tag = TagSerializer(read_only=True)
    stage = StageSerializer(read_only=True)
    assigned = UserSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)


class LinkDetailsSerializer(serializers.ModelSerializer):
    """Serializer for Task's link details"""

    class Meta:
        model = LinkDetails
        fields = ('id', 'task', 'installation_type', 'device', 'access_point', 'signal', 'ccq', 'cable',
                  'connector', 'payment', 'bill_number', 'installation_date', 'additional_details')
    read_only_fields = ('id',)


class CheckListSerializer(serializers.ModelSerializer):
    """Serialzier for Task's checklist"""

    class Meta:
        model = CheckList
        fields = ('id', 'task', 'cable', 'stand', 'router',
                  'antenna', 'router_os', 'signal', 'dns')
        read_only_fields = ('id',)


class InstallationSerializer(serializers.ModelSerializer):
    """Serialzier for Installation Tasks"""

    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )

    class Meta:
        model = Installation
        fields = ('id', 'task', 'description', 'pppoe_user',
                  'pppoe_password')
        read_only_fields = ('id',)



class TroubleshootSerializer(serializers.ModelSerializer):
    """Serialzier for Troubleshoot Tasks"""

    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )

    class Meta:
        model = Troubleshoot
        fields = ('id', 'task', 'address', 'contact', 'problem',
                  'service_charge', 'description')
        read_only_fields = ('id',)


class ChangeLocationSerializer(serializers.ModelSerializer):
    """Serialzier for Change Location Tasks"""

    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )

    class Meta:
        model = ChangeLocation
        fields = ('id', 'task', 'address', 'contact', 'service_charge', 'description')
        read_only_fields = ('id',)


class OnlineSupportSerializer(serializers.ModelSerializer):
    """Serializer for Online Support Tasks"""

    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all()
    )

    class Meta:
        model = OnlineSupport
        fields = ('id', 'task', 'contact', 'by', 'description')
        read_only_fields = ('id',)


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
        fields = ('id', 'task', 'user', 'message', 'created')
        read_only_fields = ('id',)


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

    class Meta: 
        model = Payment
        fields = ('id', 'task', 'payment', 'updated', 'created')
        read_only_fields = ('id',)

class InstallationConfirmSerializer(serializers.ModelSerializer):
    """ Serializer for InstallationConfirm"""

    class Meta: 
        model = InstallationConfirm
        fields = ('id', 'task', 'confirm', 'updated', 'created')
        read_only_fields = ('id', )