from django.db import models, connection
from django.db.models import Q
from utils.fields import EncryptedField

class EncryptedFieldManager(models.Manager):
    def enc_filter(self, *args, **kwargs):
        q_objects = Q()
        for key, value in kwargs.items():
            field = self.model._meta.get_field(key)
            if isinstance(field, EncryptedField):
                encrypted_value = field.encrypt_value_for_filtering(value)
                # Allow filtering on both encrypted and non-encrypted values
                q_objects = Q(**{key: encrypted_value})
            else:
                q_objects &= Q(**{key: value})
        return super().filter(q_objects)