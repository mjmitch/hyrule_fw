from django.shortcuts import render
from django.views.generic import TemplateView, ListView


class ViewPlayerList(TemplateView):
    template_name='players/list.html'