from django.db import models
from world_api.models import World


class Stage(models.Model):
    index = models.IntegerField()
    objective = models.CharField(max_length=300)
    movie_url = models.URLField()
    world = models.ForeignKey(World, on_delete=models.CASCADE)
