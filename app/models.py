from django.db import models

class LogEntry(models.Model):
    event_time = models.DateTimeField()
    hostname = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50)
    severity_value = models.IntegerField()
    severity = models.CharField(max_length=20)
    thread_id = models.IntegerField()
    source_name = models.CharField(max_length=100)
