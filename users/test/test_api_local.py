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

        # トークンは過去のものを使用
        token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImYyNGYzMTQ4MTk3ZWNlYTUyOTE3YzNmMTgzOGFiNWQ0ODg3ZWEwNzYiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vY29kZXBhcnR5YXV0aCIsImF1ZCI6ImNvZGVwYXJ0eWF1dGgiLCJhdXRoX3RpbWUiOjE2NDQ0MDU0MDgsInVzZXJfaWQiOiI1cVZOeUdzQndSYlA2c1RPTWdNb2p2OEpia3ExIiwic3ViIjoiNXFWTnlHc0J3UmJQNnNUT01nTW9qdjhKYmtxMSIsImlhdCI6MTY0NDQwNTQwOCwiZXhwIjoxNjQ0NDA5MDA4LCJlbWFpbCI6ImNvZGVwYXJ0eWVuam95QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJjb2RlcGFydHllbmpveUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.F0LusnEt27usvgqq6G45laXB3aSeyXh13AJvyckW_e01sw_9PxPMmbvOt0ECJbksG_xtx8JjYyFiqBpnCej05zmK2GYI3NmuyNr8B2MLNhUBFv8zGnmuf7ukkTxRzE7--Xtd0qvnaUfXUJhfewuUJJZQM2jUIYurcHNDExV_6FSQCVGnmVdUsA-tpHIfvyFtFuwXpGDKI1yVis10A9q9r2k4DZkO88eZyQ2gQG4tUx5VYXtQ_yu3yTTF98wvquQN84TlD1OVe9Qm8IzRuDGUTGGqOHWwbydrCyW7QiCcUMlyiI0bFDO83_4KigybEw5PB3tg8XaWKQuCqJFJ4E9Azw"
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token))

    def test_first_login(self):
        # 初回ログイン時の挙動確認
        # GET
        response = self.client.get("/users/auth/", content_type="application/json")
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
