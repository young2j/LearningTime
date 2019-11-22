from django.db import models

# Create your models here.
class TraditionalStrategyMemo(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '传统策略'

class AIStrategyMemo(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = 'AI策略'
