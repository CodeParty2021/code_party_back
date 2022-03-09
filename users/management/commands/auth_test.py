import requests
import pprint

# from django.test import TestCase
import os
import json
from rest_framework.test import APIClient

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = "Try to authenticate as test user"

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write("Start to authenticate as test user.")

        # クライアントを生成
        self.client = APIClient()
        token = self._generate_userToken()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token))

        # ログイン時の挙動確認
        # GET
        response = self.client.get("/users/auth/", content_type="application/json")

        # レスポンスのステータスコードをチェック
        if response.status_code == 200:
            self.stdout.write("Response: OK")
        else:
            self.stdout.write("Response: NG")
            return

        # jsonをデコード
        data = json.loads(response.content.decode("utf-8"))
        # データチェック
        if data["userInfo"]["id"]:
            self.stdout.write("ユーザ情報: 正常に取得できました．")
        else:
            self.stdout.write("ユーザ情報: 取得できませんでした．")
            return

        self.stdout.write("【認証情報】")
        self.stdout.write(f"Token : {token}")
        self.stdout.write("【ユーザ情報】")
        self.stdout.write(str(data))
        self.stdout.write("＜＜テストは正常に終了しました．＞＞")

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
