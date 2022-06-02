from django.db import models

from stage_api.models import Stage

# Create your models here.


class Step(models.Model):
    objective = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    index = models.IntegerField()
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)

    option = models.JSONField(default={}, blank=True)
    opponents = models.ManyToManyField(
        "code_api.code", related_name="opponents", blank=True, default=[]
    )
