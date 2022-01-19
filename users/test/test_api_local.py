import requests
import pprint
from django.test import TestCase
import os
import json
from rest_framework.test import APIClient

"""
# 参考記事 https://qiita.com/DeliciousBar/items/d6845d329e37f21a6d4f
class AuthAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        token = self._generate_userToken()
        print(token)
        self.client.credentials(
            HTTP_Authorization="Bearer {}".format(
                "eyJhbGciOiJSUzI1NiIsImtpZCI6IjQwMTU0NmJkMWRhMzA0ZDc2NGNmZWUzYTJhZTVjZDBlNGY2ZjgyN2IiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiYWtpaGl0byBpaGFyYSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQVRYQUp3SVRhUU9PdmMtLVRncjlkOXZ3SUpFaUtFaWtXRWhGdC1RYnZMdD1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9jb2RlcGFydHlhdXRoIiwiYXVkIjoiY29kZXBhcnR5YXV0aCIsImF1dGhfdGltZSI6MTY0MTAxMTMwMiwidXNlcl9pZCI6ImlIRDNSTmVzazRQQWowU21VdzJVbnk4M0lhaTIiLCJzdWIiOiJpSEQzUk5lc2s0UEFqMFNtVXcyVW55ODNJYWkyIiwiaWF0IjoxNjQyNTExMzM1LCJleHAiOjE2NDI1MTQ5MzUsImVtYWlsIjoiYWtpdGVydXRvQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTA0NDgyOTQ0OTYzODc0NTgzNzIyIl0sImVtYWlsIjpbImFraXRlcnV0b0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.txLNYLDjO0k_vZOmbajvecrgTdY6nzh7dCu6oGF3KSGhcNvX8GVxiBM-OFGrwMvABi8vilIOpWrgiv5u7Aje7oHB9J7esHUeLRqdCHi_DuVObyMbLHb7i62ROSXzmTxPm-tjCXb0CjZOJEW7h3fbomaUTsMDWHZDesaxZ6kylfHiZYKF4F9YlYCmLtrJ85q3PPfhOV1dIC_bQNwYU58EcEy7fm-N68VX45sAJkG-kXS3JqK_kv9smXNy119O3QHRKttW_Nq5xxjPwZwtrboTnwWxtmxhKedzBr-whjR7XAVvL1-stIm2TNa1EvzLPJuB-6HjVIR_aJ5HTr5AfBfhAw"
            )
        )
        print(self.client._credentials)

    def test_first_login(self):
        #初回ログイン時の挙動確認
        # GET
        response = self.client.get("/users/auth/", content_type="application/json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)

        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        print(body)
        self.assertEquals(
        _    body,
            [
                {
                    "user_info": {
                        "id": "fweew",
                        "displayName": "enjoy",
                        "email": "sample@sample.com",
                        "picture": "feawef.com",
                    },
                    "created": True,
                }
            ],
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
"""
