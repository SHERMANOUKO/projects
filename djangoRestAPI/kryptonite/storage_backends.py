from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class AgentProfileMediaStorage(S3Boto3Storage):
    """store agent profile pictures"""
    location = settings.AWS_AGENT_PROFILE_MEDIA_LOCATION

class LandlordProfileMediaStorage(S3Boto3Storage):
    """store landlord profile pictures"""
    location = settings.AWS_LANDLORD_PROFILE_MEDIA_LOCATION

class CaretakerProfileMediaStorage(S3Boto3Storage):
    """store caretaker profile pictures"""
    location = settings.AWS_CARETAKER_PROFILE_MEDIA_LOCATION

class TenantProfileMediaStorage(S3Boto3Storage):
    """store tenant profile pictures"""
    location = settings.AWS_TENANT_PROFILE_MEDIA_LOCATION

class ApartmentMediaStorage(S3Boto3Storage):
    """store apartment pictures"""
    location = settings.AWS_APARTMENT_MEDIA_LOCATION
    default_acl = 'public-read'

class PropertyMediaStorage(S3Boto3Storage):
    """store property pictures"""
    location = settings.AWS_PROPERTY_MEDIA_LOCATION
    default_acl = 'public-read'

class MediaStorage(S3Boto3Storage):
    """store other media"""
    location = 'media'
    file_overwrite = False