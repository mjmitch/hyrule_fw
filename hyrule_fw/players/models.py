from django.db import models
from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT

from django.contrib.auth.models import User

class Rank(models.Model):
    name = models.CharField(max_length=24)
    officer_perms = models.BooleanField(default=False)
    admin_perms = models.BooleanField(default=False)
    default = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class CharacterClass(models.Model):
    name = models.CharField(max_length=24)
    image = models.ImageField(upload_to=MEDIA_ROOT+'images/character_classes')

    def __unicode__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=40)
    main_id = models.IntegerField(blank=True, null=True)
    rank = models.ForeignKey(Rank, blank=True)
    approved = models.BooleanField(default=False)
    user = models.ForeignKey(User)

    def main(self):
        for char in self.character_set.all():
            if char.is_main:
                self.main_id = char.id
                return char
        return None

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.main():
            for char in self.character_set.all():
                char.is_main = False
            self.main().is_main = True
        if not self.rank and self.approved:
            self.rank = Rank.objects.get(default=True)
        super(Player, self).save(*args, **kwargs)


class Character(models.Model):
    name = models.CharField(max_length=40)
    character_class = models.ForeignKey(CharacterClass)
    player = models.ForeignKey(Player)
    is_main = models.BooleanField(default=False)
    level = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.level > 80:
            self.level = 80
        super(Character, self).save(*args, **kwargs)