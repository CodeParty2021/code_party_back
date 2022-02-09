import requests
import pprint
from django.test import TestCase
import os
import json
from rest_framework.test import APIClient


# 参考記事 https://qiita.com/DeliciousBar/items/d6845d329e37f21a6d4f
class AuthAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        token = self._generate_userToken()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token))

    def test_first_login(self):
        # 初回ログイン時の挙動確認
        # GET
        response = self.client.get("/users/auth", content_type="application/json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)

        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            {
                "userInfo": {
                    "id": "5qVNyGsBwRbP6sTOMgMojv8Jbkq1",
                    "displayName": "名無しオペレータ cod",
                    "email": "codepartyenjoy@gmail.com",
                    "picture": "",
                },
                "created": True,
            },
        )

    def _generate_userToken(self):
        API_KEY = os.getenv("API_KEY")
        TEST_FIREBASE_EMAIL = os.getenv("TEST_FIREBASE_EMAIL")
        TEST_FIREBASE_PASSWORD = os.getenv("TEST_FIREBASE_PASSWORD")
        uri = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={API_KEY}"
        data = {
            "email": TEST_FIREBASE_EMAIL,
            "password": TEST_FIREBASE_PASSWORD,
            "returnSecureToken": True,
        }
        result = requests.post(url=uri, data=data).json()
        return result["idToken"]
