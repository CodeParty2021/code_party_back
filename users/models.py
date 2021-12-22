from django.db import models

# Create your models here.

# 既存userとコンフリクトするので


class User(models.Model):
    id = models.CharField(primary_key=True)  # firebase のuidをUserモデルの主キーにする
    display_name = models.CharField(max_length=32)  # 表示名
    photo_url = models.CharField()  # ユーザー画像, firebase上に存在
