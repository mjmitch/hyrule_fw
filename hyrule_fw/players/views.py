from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from models import *


class ViewPlayerList(TemplateView):
    template_name='players/list.html'

    def get_context_data(self, **kwargs):
        default_rank = Rank.objects.get(name="default")
        officer_rank = Rank.objects.get(name="Officer")
        admin_rank = Rank.objects.get(name="Admin")
        vice_rank = Rank.objects.get(name="Vice Lead")
        lead_rank = Rank.objects.get(name="Guild Lead")
        members = Player.objects.filter(rank=default_rank)
        officers = Player.objects.filter(rank=officer_rank)
        admins = Player.objects.filter(rank=admin_rank)
        vices = Player.objects.filter(rank=vice_rank)
        lead = Player.objects.filter(rank=lead_rank)
        data = {
            'members': members,
            'officers': officers,
            'vices': vices,
            'admins': admins,
            'Guild Lead': lead,
        }
        context = super(ViewPlayerList, self).get_context_data(**kwargs)
        context['player_data'] = data
        return context