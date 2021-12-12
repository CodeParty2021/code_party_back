from django.db import models


class Stage(models.Model):
    name = models.CharField(max_length=32)
    stage_index = models.IntegerField()
    rule = models.CharField(max_length=300)
