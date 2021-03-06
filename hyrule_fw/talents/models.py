from django.db import models
from hyrule_fw.gp.models import CharacterClass, Character


class TalentTreeType(models.Model):
    name = models.CharField(max_length=24)
    character_class = models.ForeignKey(CharacterClass)


class TalentType(models.Model):
    name = models.CharField(max_length=24)
    talent_tree_type = models.ForeignKey(TalentTreeType)
    description = models.TextField()
    max_points = models.PositiveSmallIntegerField()
    has_rune = models.BooleanField(default=False)
    required_points = models.PositiveIntegerField()
    x_position = models.PositiveSmallIntegerField(help_text='Left-Most position is Position #1 (Right-Most is #4)')
    has_parent = models.BooleanField(default=False)
    parent_id = models.PositiveIntegerField(blank=True)
    parent_requirements = models.PositiveSmallIntegerField(default=0, help_text='How many points does the parent ' +
                                                                                'talent need to have to activate ' +
                                                                                'this talent? Leave value at "0" if ' +
                                                                                'there is no parent talent.')

    def find_parent(self):
        closest_points = self.required_points
        closest = None
        for talent in self.talent_tree_type.talenttype_set.all():
            if self.x_position == talent.x_position and self.required_points > talent.required_points:
                dist = self.required_points - talent.required_points
                if dist < closest_points:
                    closest_points = dist
                    closest = talent.id
        return closest

    def save(self, *args, **kwargs):
        if self.has_parent and not self.parent_id:
            self.parent_id = self.find_parent()
        super(TalentType, self).save(*args, **kwargs)


class Talent(models.Model):
    name = models.CharField(max_length=24, blank=True)
    talent_type = models.ForeignKey(TalentType)
    points = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.points > self.talent_type.max_points:
            self.points = self.talent_type.max_points
        super(Talent, self).save(*args, **kwargs)


class TalentTree(models.Model):
    name = models.CharField(max_length=60, blank=True)
    talent_tree_type = models.ForeignKey(TalentTreeType)
    character = models.ForeignKey(Character)