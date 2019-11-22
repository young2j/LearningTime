from django.contrib import admin
import xadmin
from .models import TraditionalStrategy,AIStrategy
# Register your models here.
@xadmin.sites.register(TraditionalStrategy)
class TraditionalStrategyAdmin(object):
    pass

@xadmin.sites.register(AIStrategy)
class AIStrategy(object):
    pass