from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class TraditionalSelection(models.Model):
    '''
    ...
    '''
    # def __str__(self):
        # return self.name

    class Meta:
        verbose_name = verbose_name_plural = "传统策略"

class AISelection(models.Model):
    '''
    ...
    '''
    class Meta:
        verbose_name = verbose_name_plural = "AI策略"