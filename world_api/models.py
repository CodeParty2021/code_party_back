from django.db import models


class World(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=300)
    movie_url = models.URLField()
    index = models.IntegerField()
