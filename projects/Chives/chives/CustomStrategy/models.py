from django.db import models

# Create your models here.
class CustomSelection(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '选股'

class CustomBacktest(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '回测'