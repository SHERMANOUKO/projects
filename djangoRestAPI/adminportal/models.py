import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from kryptonite.storage_backends import AgentProfileMediaStorage, LandlordProfileMediaStorage, \
    CaretakerProfileMediaStorage, ApartmentMediaStorage, TenantProfileMediaStorage, \
    PropertyMediaStorage
from .managers import CustomUserManager
# from adminportal.services.imageconverter import image_converter

# Create your models here.

class CustomUser(AbstractUser):
    ADMIN = 'ADMIN'
    AGENT = 'AGENT'
    CARETAKER = 'CARETAKER'
    LANDLORD = 'LANDLORD'
    PUBLIC = 'PUBLIC'

    USER_CHOICES = [
        (ADMIN, 'Admin'),
        (AGENT, 'Agent'),
        (CARETAKER, 'Caretaker'),
        (LANDLORD, 'Landlord'),
        (PUBLIC, 'Public')
    ]

    user_type = models.CharField(max_length=50, choices=USER_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(null=True, unique=True)
    first_name = None
    last_name = None

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class TokenModel(models.Model):
    key = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

class Regions(models.Model):
    regionID = models.AutoField(primary_key=True)
    regionCounty = models.CharField(max_length=255)
    regionName = models.CharField(max_length=255, unique=True)

class Agents(models.Model):

    def _image_file_name(instance, filename):
        # ext = filename.split('.')[-1]
        ext = 'jpg'
        filename = '%s.%s' % (instance.agentNationalID, ext)
        return filename

    agentID = models.AutoField(primary_key=True)
    agentNationalID = models.IntegerField(unique=True)
    agentName = models.CharField(max_length=255)
    agentAvatar = models.ImageField(storage=AgentProfileMediaStorage(), upload_to=_image_file_name)
    agentPhoneNumber = models.IntegerField(unique=True)
    username = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

class Branches(models.Model):
    branchID = models.AutoField(primary_key=True)
    branchName = models.CharField(max_length=255)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL, blank=True, null=True)
    agent = models.OneToOneField(Agents, on_delete=models.SET_NULL, blank=True, null=True)
    branchEmailAddress = models.EmailField(unique=True)
    branchPhoneNumber = models.IntegerField(unique=True)
    branchBuildingLocation = models.CharField(max_length=100)
    branchLatitude = models.FloatField(null=True)
    branchLongitude = models.FloatField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['region', 'branchName'], name='unique_region_name')
        ]

class Landlords(models.Model):
    def _image_file_name(instance, filename):
        # ext = filename.split('.')[-1]
        ext = 'jpg'
        filename = '%s.%s' % (instance.landlordNationalID, ext)
        return filename

    landlordID = models.AutoField(primary_key=True)
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE, to_field='username')
    landlordName = models.CharField(max_length=255)
    landlordNationalID = models.IntegerField(unique=True)
    landlordEmailAddress = models.EmailField(null=True, unique=True) 
    landlordPrimaryPhoneNumber = models.IntegerField(unique=True)   
    landlordSecondaryPhoneNumber = models.IntegerField(null=True)
    landlordAvatar = models.ImageField(storage=LandlordProfileMediaStorage(), upload_to=_image_file_name)

class Caretakers(models.Model):
    def _image_file_name(instance, filename):
        # ext = filename.split('.')[-1]
        ext = 'jpg'
        filename = '%s.%s' % (instance.caretakerNationalID, ext)
        return filename

    caretakerID = models.AutoField(primary_key=True)
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE, to_field='username')
    caretakerName = models.CharField(max_length=255)
    branch = models.ForeignKey(Branches, on_delete=models.SET_NULL, blank=True, null=True)
    caretakerNationalID = models.IntegerField(unique=True)
    caretakerAvatar = models.ImageField(storage=CaretakerProfileMediaStorage(), upload_to=_image_file_name)
    caretakerPhoneNumber = models.IntegerField(unique=True)

class Apartments(models.Model):
    def _image_file_name(instance, filename):
        # ext = filename.split('.')[-1]
        ext = 'jpg'
        filename = '%s/%s/%s.%s' % (
            instance.apartmentCounty,
            instance.branch.branchID,
            instance.apartmentID,
            ext
        )
        return filename

    apartmentID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    landlord = models.ForeignKey(Landlords, on_delete=models.SET_NULL, blank=True, null=True)
    apartmentName = models.CharField(max_length=255)
    apartmentCounty = models.CharField(max_length=255)
    apartmentEstate = models.CharField(max_length=255)
    branch = models.ForeignKey(Branches, on_delete=models.SET_NULL, null=True, blank=True)
    apartmentLatitude = models.FloatField(null=True)
    apartmentLongitude = models.FloatField(null=True)
    apartmentStudentType = models.BooleanField(default=False)
    caretaker = models.ForeignKey(Caretakers, on_delete=models.SET_NULL, blank=True, null=True)
    apartmentAvatar = models.ImageField(storage=ApartmentMediaStorage(), upload_to=_image_file_name)

