from django.db import models

from stage_api.models import Stage

# Create your models here.


class Step(models.Model):
    objective = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    index = models.IntegerField()
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)

    option = models.JSONField(default={})


class StepCode(models.Model):
    # コード
    code = models.ForeignKey("code_api.code", on_delete=models.SET_NULL, null=True)
    # ステップ
    step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True)
