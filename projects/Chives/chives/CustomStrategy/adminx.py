from django.contrib import admin
import xadmin
from .models import CustomSelection,CustomBacktest
# Register your models here.
@xadmin.sites.register(CustomSelection)
class CustomSelectionAdmin(object):
    pass


@xadmin.sites.register(CustomBacktest)
class CustomBacktestAdmin(object):
    pass