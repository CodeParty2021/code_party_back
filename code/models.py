
from django.db import models


class Code(models.Model):
    name = models.CharField(max_length=32)
    user = models.IntegerField()
    file_path = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=16)

class Result(models.Model):
    json_path = models.CharField(max_length=128)
    
class ResultCode(models.Model):
    result = models.IntegerField()
    code = models.IntegerField()
    