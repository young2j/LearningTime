from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    '''
    首页视图
    '''
    template_name = 'index/index.html'