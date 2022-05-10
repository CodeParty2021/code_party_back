from django.db import models


class User(models.Model):
    id = models.CharField(
        primary_key=True, max_length=300
    )  # firebase のuidをUserモデルの主キーにする
    display_name = models.CharField(max_length=64)  # 表示名
    email = models.EmailField(null=True)
    picture = models.CharField(max_length=300, null=True)  # ユーザー画像, firebase上に存在
    is_staff = models.BooleanField(default=False)  # ユーザーがスタッフユーザーでない
