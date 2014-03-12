from django.db import models


class EventType(models.Model):
    name = models.CharField(max_length=64)
    default_dkp_reward = models.PositiveIntegerField(blank=True)
    image = models.ImageField(upload_to='images/events', blank=True)


class Event(models.Model):
    event_type = models.ForeignKey(EventType)
    start_date = models.DateField()
    start_time = models.TimeField()
    dkp = models.PositiveIntegerField(blank=True)

    def save(self, *args, **kwargs):
        if not self.dkp and self.event_type.default_dkp_reward:
            self.dkp = self.event_type.default_dkp_reward
        super(Event, self).save(*args, **kwargs)