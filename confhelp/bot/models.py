from django.db import models
import datetime


class EventCalendar(models.Model):
    event_date_start = models.DateTimeField()
    event_date_end = models.DateTimeField()
    reporter = models.IntegerField()
    speech_topic = models.TextField()


class EventDate(models.Model):
    event_time_start = models.ForeignKey(EventCalendar, on_delete=models.CASCADE)
    event_time_stop = models.ForeignKey(EventCalendar, on_delete=models.CASCADE)
    




