from django.views.generic import TemplateView, ListView
from models import *
from django.http import Http404


class ViewPlayerList(ListView):
    template_name='players/list.html'

    def get_queryset(self):
        return Player.objects.all().order_by('-name')


class ViewRankList(ListView):
    template_name = 'players/list.html'

    def get_queryset(self):
        return Rank.objects.all()


class ViewPlayer(ListView):
    template_name = 'players/player.html'

    def get_player(self):
        try:
            return Player.objects.get(id=self.args[0])
        except:
            return None

    def get_queryset(self):
        player = self.get_player()
        if not player:
            raise Http404
        return Character.objects.filter(player=player)

class ViewRank(ListView):
    template_name = 'players/rank.html'

    def get_rank(self):
        try:
            return Rank.objects.get(id=self.args[0])
        except:
            return None

    def get_queryset(self):
        rank = self.get_rank()
        if not rank:
            raise Http404
        return Player.objects.filter(rank=rank)