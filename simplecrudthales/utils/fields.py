from django.db import models
from .thales import *
import logging

logger = logging.getLogger(__name__)

class EncryptedField(models.TextField):
    def get_prep_value(self, value):
        if value is None:
            return value
        value = thales_encrypt(value)
        return value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        
        try:
            return thales_decrypt(value)
        except Exception:
            return value
    
    def encrypt_value_for_filtering(self, value):
        value = thales_encrypt(value)
        return value