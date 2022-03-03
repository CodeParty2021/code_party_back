from django.db import models


class User(models.Model):
    id = models.CharField(
        primary_key=True, max_length=300
    )  # firebase のuidをUserモデルの主キーにする
    display_name = models.CharField(max_length=64)  # 表示名
    email = models.EmailField()
    picture = models.CharField(max_length=300)  # ユーザー画像, firebase上に存在
    is_stuff = models.BooleanField(default=False)  # ユーザーがスタッフユーザーでない
