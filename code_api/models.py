import uuid
from django.db import models

from step_api.models import Step
from users.models import User


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=20)


class Code(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_content = models.TextField()

    # タイムスタンプ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #外部キー
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.SET_NULL, null=True)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# データベースには格納しないためobjectを継承
# class CodeRunResult(object):
#     def __init__(self, unity_url, json_id):
#         self.unity_url = unity_url
#         self.json_id = json_id