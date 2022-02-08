from django.db import models

from stage_api.models import Stage

# Create your models here.
class Step(models.Model):
    id = models.IntegerField(primary_key=True)
    objective = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    index = models.IntegerField()
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
