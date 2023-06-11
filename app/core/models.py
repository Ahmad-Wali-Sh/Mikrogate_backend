from email.policy import default
from io import open_code
from unicodedata import name
import uuid
import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.conf import settings
from django.template.defaultfilters import date

def user_avatar_file_path(instance, filename):
    """Generate file path for new user avatar"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'user', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports emial instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(null=True, upload_to=user_avatar_file_path)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name


class Router(models.Model):
    """Device to bes used in a contract"""
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    available = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Antenna(models.Model):
    """Device to bes used in a contract"""
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    available = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name






class Package(models.Model):
    """Package to be used in a contract"""
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    price = models.IntegerField()
    available = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Contracts(models.Model):
    """Contracts Objects"""

    """PESONAL INFO"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    contract_number = models.CharField(max_length=50, unique=True)
    contract_id = models.CharField(max_length=50, blank=True)
    contract_type = models.ForeignKey("ContractTypes", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    referral = models.CharField(max_length=50, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(default=datetime.now())
    activation = models.DateTimeField(default=datetime.now())
    valid = models.DateTimeField(default=datetime.now() + relativedelta(years=1))
    status = models.ForeignKey("ContractStatus", on_delete=models.CASCADE)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ContractTypes(models.Model):
    """Contract Types"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ContractPackage(models.Model):
    """Contract's Package"""
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    price = models.CharField(max_length=255, blank=True)


class ContractAntenna(models.Model):
    """Contract's Antenna"""
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    antenna = models.ForeignKey(Antenna, on_delete=models.CASCADE)
    condition = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    Lease_amount = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    collected = models.BooleanField(default=False)



class ContractRouter(models.Model):
    """Contract's Router"""
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    router = models.ForeignKey(Router, on_delete=models.CASCADE)
    condition = models.CharField(max_length=255, blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    Lease_amount = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    collected = models.BooleanField(default=False)


class ContractPayment(models.Model):
    """Contract payment object"""
    contract = models.ForeignKey("Contracts", on_delete=models.CASCADE)
    payment_total = models.IntegerField(default=0)
    service_charge = models.IntegerField(default=0)
    other_charges = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    lease_deposit = models.IntegerField(default=0)
    grand_total = models.IntegerField(default=0)
    currency = models.ForeignKey("ContractCurrency", on_delete=models.DO_NOTHING)


class ContractOtherService(models.Model):
    """Contract other service object"""
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    payment_method = models.CharField(max_length=100, blank=True)
    price = models.IntegerField(blank=True)


class ContractCurrency(models.Model):
    """Contract currency object"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name




class ContractStatus(models.Model):
    """Contract status object"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Notifications(models.Model):
    user_sender=models.ForeignKey(User,null=True,blank=True,related_name='user_sender',on_delete=models.CASCADE)
    user_revoker=models.ForeignKey(User,null=True,blank=True,related_name='user_revoker',on_delete=models.CASCADE)
    status=models.CharField(max_length=264,null=True,blank=True,default="unread")
    type_of_notification=models.CharField(max_length=264,null=True,blank=True)


# class Contract(models.Model):
#     """Contract object"""

#     CHOICES = (
#         ('new', 'New'),
#         ('done', 'Done'),
#         ('in-progress', 'In-Progress'),
#         ('pending', 'Pending'),
#         ('canceled', 'Canceled'),
#         ('expired', 'Expired'),
#     )

#     today = datetime.now()
#     add1year = today + relativedelta(years=1)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         null=True,
#         default=1
#     )
#     referral = models.CharField(max_length=255, blank=True, null=True)
#     contract_no = models.CharField(max_length=255, null=True)
#     contract_id = models.CharField(max_length=255, blank=True, null=True)
#     contract_date = models.DateTimeField(default=today)
#     activation_date = models.DateTimeField(null=True)
#     valid_upto = models.DateTimeField(default=add1year)
#     # valid_upto = models.DateTimeField(null=True)
#     organization = models.CharField(max_length=255, blank=True, null=True)
#     contract_type = models.CharField(max_length=255, blank=True, null=True)
#     poc_name = models.CharField(max_length=255, null=True)
#     poc_number = models.CharField(max_length=100, null=True)
#     poc_email = models.EmailField(blank=True, null=True)
#     address = models.CharField(max_length=255, null=True)
#     # packages = models.ManyToManyField('Package', blank=True)
#     packages = models.CharField(max_length=255, null=True)
#     package_price = models.CharField(max_length=255, blank=True, null=True)
#     # router = models.ManyToManyField('Router', blank=True)
#     router = models.CharField(max_length=255, null=True)
#     # antenna = models.ManyToManyField('Antenna', blank=True)
#     antenna = models.CharField(max_length=255, null=True)
#     # customerDevices = models.CharField(max_length=255, null=True)
#     rou_cond = models.CharField(max_length=255, blank=True, null=True)
#     rou_dec = models.CharField(max_length=255, blank=True, null=True)
#     rou_qty = models.CharField(max_length=255, blank=True, null=True)
#     rou_amnt = models.CharField(max_length=255, blank=True, null=True)
#     rou_lease_amnt = models.CharField(max_length=255, blank=True, null=True)
#     rou_amnt_totl = models.CharField(max_length=255, blank=True, null=True)
#     rou_collected = models.BooleanField(blank=True, null=True)
#     ann_cond = models.CharField(max_length=255, blank=True, null=True)
#     ann_dec = models.CharField(max_length=255, blank=True, null=True)
#     ann_qty = models.CharField(max_length=255, blank=True, null=True)
#     ann_amnt = models.CharField(max_length=255, blank=True, null=True)
#     ann_lease_amnt = models.CharField(max_length=255, blank=True, null=True)
#     ann_amnt_totl = models.CharField(max_length=255, blank=True, null=True)
#     ann_collected = models.BooleanField(blank=True, null=True, default=0)
#     cable = models.CharField(max_length=255, blank=True, null=True)
#     cable_cond = models.CharField(max_length=255, blank=True, null=True)
#     cable_collected = models.BooleanField(blank=True, null=True, default=0)
#     other_service = models.CharField(max_length=255, blank=True, null=True)
#     other_dec = models.CharField(max_length=255, blank=True, null=True)
#     other_pay_method = models.CharField(max_length=255, blank=True, null=True)
#     other_qty = models.CharField(max_length=255, blank=True, null=True)
#     other_price = models.CharField(max_length=255, blank=True, null=True)
#     payment_total = models.CharField(max_length=255, blank=True, null=True)
#     service_charge = models.CharField(max_length=255, blank=True, null=True)
#     other_charges = models.CharField(max_length=255, blank=True, null=True)
#     discount = models.CharField(max_length=255, blank=True, null=True)
#     lease_deposit = models.CharField(max_length=255, blank=True, null=True)
#     grand_total = models.CharField(max_length=255, blank=True, null=True)
#     curren = models.CharField(
#         max_length=255, blank=True, null=True, default='AFN')
#     note = models.TextField(blank=True, null=True)
#     status = models.CharField(
#         max_length=15, choices=CHOICES, default='pending', null=True)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.contract_no


class Log(models.Model):
    """Contract Log Object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    contract = models.CharField(max_length=255)
    log = models.CharField(max_length=255)
    updated = models.DateTimeField(auto_now=True)


class Project(models.Model):
    """Taskmanager project object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Stage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    title = models.CharField(max_length=255)
    contract = models.ForeignKey(
        Contracts, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
    deadline = models.DateTimeField()
    stage = models.ForeignKey(Stage, on_delete=models.DO_NOTHING)
    assigned = models.ManyToManyField(User, related_name="Task")
    description = models.TextField(null=True)
    read = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title

class LinkDetails(models.Model):
    """Link Details Object"""
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    installation_type = models.CharField(max_length=100, blank=True)
    device = models.CharField(max_length=255, blank=True)
    access_point = models.CharField(max_length=10, blank=True)
    signal = models.CharField(max_length=10, blank=True)
    ccq = models.CharField(max_length=10, blank=True)
    cable = models.IntegerField(null=True, blank=True)
    connector = models.IntegerField(null=True, blank=True)
    payment = models.IntegerField(null=True, blank=True)
    bill_number = models.IntegerField(null=True, blank=True)
    installation_date = models.DateTimeField()
    additional_details = models.TextField(blank=True)


class CheckList(models.Model):
    """Link Checklist Object"""
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    cable = models.BooleanField(default=False)
    stand = models.BooleanField(default=False)
    router = models.BooleanField(default=False)
    antenna = models.BooleanField(default=False)
    router_os = models.BooleanField(default=False)
    signal = models.BooleanField(default=False)
    dns = models.BooleanField(default=False)


class Installation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True)
    pppoe_user = models.CharField(max_length=50, blank=True)
    pppoe_password = models.CharField(max_length=50, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']


class Troubleshoot(models.Model):
    """Task-Manager Troubleshoot Object"""
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    problem = models.CharField(max_length=255)
    service_charge = models.IntegerField()
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']


class ChangeLocation(models.Model):
    """Task-Manager Change Location Object"""
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    service_charge = models.IntegerField()
    description = models.TextField(default='')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']


class OnlineSupport(models.Model):
    """Task-Manager Online Support Object"""
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    contact = models.CharField(max_length=20)
    by = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']


class Amendment(models.Model):
    """Task-Manager Amendment object"""
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    message = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']


class TaskLog(models.Model):
    """Task-Manager Log Object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body


class Message(models.Model):
    """Task-Manager Message Object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    to = models.ManyToManyField(User, related_name='messages')
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body