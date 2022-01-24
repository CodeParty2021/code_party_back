from django.db import models


class Stage(models.Model):
    stage_index = models.IntegerField()
    objective = models.CharField(max_length=300)
    movie_url = models.URLField()
