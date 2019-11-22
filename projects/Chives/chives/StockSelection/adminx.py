from django.contrib import admin

import xadmin
from .models import TraditionalSelection,AISelection
# Register your models here.
@xadmin.sites.register(TraditionalSelection)
class TraditionalSelectionAdmin(object):
    pass

@xadmin.sites.register(AISelection)
class AISelectionAdmin(object):
    pass
