from django.db import models
import uuid

from utils.fields import EncryptedField
from utils.managers import EncryptedFieldManager

# Create your models here.
class User(models.Model):
    id = models.CharField(
        primary_key=True, 
        max_length=36, 
        default=uuid.uuid4, 
        editable=False
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    ktp = EncryptedField()
    npwp = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    birth_day = models.CharField(max_length=255, blank=True, null=True)
    birth_place = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    create_by = models.CharField(max_length=255, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True)
    update_by = models.CharField(max_length=255, blank=True, null=True)
    expired_date = models.DateTimeField(blank=True, null=True)
    deleted_date = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=255, blank=True, null=True)

    objects=EncryptedFieldManager()

    def __str__(self):
        return self.full_name
