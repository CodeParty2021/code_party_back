import uuid
from django.db import models

from step_api.models import Step
from code_api.models import Code


class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    json_path = models.CharField(max_length=200)

    # タイムスタンプ
    created_at = models.DateTimeField(auto_now_add=True)

    # 外部キー
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    codes = models.ManyToManyField(Code)
