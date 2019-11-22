from django.contrib import admin
import xadmin
from .models import TraditionalStrategyMemo,AIStrategyMemo
# Register your models here.
@xadmin.sites.register(TraditionalStrategyMemo)
class TraditionalStrategyMemoAdmin(object):
    pass

@xadmin.sites.register(AIStrategyMemo)
class AIStrategyMemoAdmin(object):
    pass

