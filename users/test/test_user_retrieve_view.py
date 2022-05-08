from django.test import TestCase
from rest_framework.test import APIClient
from users.models import User
import json


class UserAPITests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        # クライアント作成(TODO:ログイン必須になった場合，修正が必要)
        self.client = APIClient(enforce_csrf_checks=True)

        # データ準備
        User.objects.create(
            id="testuid", display_name="test user", picture="https://hoge.com/"
        )

    def test_get_user(self):
        """ID="testuid"のステージを取得"""
        # GET
        response = self.client.get("/users/testuid/", format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            {
                "id": "testuid",
                "displayName": "test user",
                "picture": "https://hoge.com/",
                "isStaff": False,
            },
        )

    def test_Display_Name_Update(self):
        self.user1 = User.objects.create(
            display_name="hello",
            picture="http://localhost:8000/users/auth",
            is_staff=True,
        )
        # ユーザ強制ログイン
        self.client.force_authenticate(user=self.user1)
        """Display_nameの変更"""
        # PATCH
        response = self.client.patch(
            f"/users/update/",
            {"displayName": "changed user"},
            format="json",
        )

        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            {
                "displayName": "changed user",
                "picture": "http://localhost:8000/users/auth",
                "isStaff": True,
            },
        )
