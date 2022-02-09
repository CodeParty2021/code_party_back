from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from firebase_admin import auth
from firebase_admin._auth_utils import InvalidIdTokenError

from .models import User


# 認証クラスBaseAuthenticationを継承することでカスタムできる
class FirebaseAuthentication(BaseAuthentication):
    keyword = "Bearer"
    model = None

    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()  # headerがここ
        # ログインの例外処理
        if not auth_header or auth_header[0].lower() != self.keyword.lower().encode():
            return None  # 認証なし

        if len(auth_header) == 1:  # 認証の中身なし
            msg = "Authorization 無効"
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:  # tokenにスペースが含まれている
            msg = "Authorization 無効 スペースはない"
            raise exceptions.AuthenticationFailed(msg)

        try:
            id_token = auth_header[1].decode()  # firebase jwtの取り出し
            decoded_token = auth.verify_id_token(id_token)  # firebase jwtの認証

            # それぞれ取り出し。 本来はここもSerializerでやるべき？
            uid = decoded_token["uid"]
            # name がない可能性がある。
            if "name" in decoded_token:
                display_name = decoded_token["name"]
            else:
                # 名前がなければemailの頭文字3つ
                display_name = "名無しオペレータ " + decoded_token["email"][0:3]
            email = decoded_token["email"]

            # pictureがない可能性がある
            if "picture" in decoded_token:
                picture = decoded_token["picture"]
            else:
                picture = ""

            try:  # ただのログイン
                user = User.objects.get(pk=uid)
                return (user, {"created": False})
            except User.DoesNotExist:  # 新規登録したとき
                user = User.objects.create(
                    id=uid, display_name=display_name, email=email, picture=picture
                )
                return (user, {"created": True})

        except InvalidIdTokenError:
            msg = "不正なfirebaseTokenです。"
            raise exceptions.AuthenticationFailed(msg)

    def authenticate_header(self, request):
        pass


"""
curl -H GET 'http://localhost:8000/users/auth' -H 'Content-Type:application/json;charset=utf-8' -H 'Authorization: Beaner eyJhbGciOiJSUzI1NiIsImtpZCI6IjQwMTU0NmJkMWRhMzA0ZDc2NGNmZWUzYTJhZTVjZDBlNGY2ZjgyN2IiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiYWtpaGl0byBpaGFyYSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQVRYQUp3SVRhUU9PdmMtLVRncjlkOXZ3SUpFaUtFaWtXRWhGdC1RYnZMdD1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9jb2RlcGFydHlhdXRoIiwiYXVkIjoiY29kZXBhcnR5YXV0aCIsImF1dGhfdGltZSI6MTY0MTAxMTMwMiwidXNlcl9pZCI6ImlIRDNSTmVzazRQQWowU21VdzJVbnk4M0lhaTIiLCJzdWIiOiJpSEQzUk5lc2s0UEFqMFNtVXcyVW55ODNJYWkyIiwiaWF0IjoxNjQyNTExMzM1LCJleHAiOjE2NDI1MTQ5MzUsImVtYWlsIjoiYWtpdGVydXRvQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTA0NDgyOTQ0OTYzODc0NTgzNzIyIl0sImVtYWlsIjpbImFraXRlcnV0b0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.txLNYLDjO0k_vZOmbajvecrgTdY6nzh7dCu6oGF3KSGhcNvX8GVxiBM-OFGrwMvABi8vilIOpWrgiv5u7Aje7oHB9J7esHUeLRqdCHi_DuVObyMbLHb7i62ROSXzmTxPm-tjCXb0CjZOJEW7h3fbomaUTsMDWHZDesaxZ6kylfHiZYKF4F9YlYCmLtrJ85q3PPfhOV1dIC_bQNwYU58EcEy7fm-N68VX45sAJkG-kXS3JqK_kv9smXNy119O3QHRKttW_Nq5xxjPwZwtrboTnwWxtmxhKedzBr-whjR7XAVvL1-stIm2TNa1EvzLPJuB-6HjVIR_aJ5HTr5AfBfhAw
' | jq .

eyJhbGciOiJSUzI1NiIsImtpZCI6IjQwMTU0NmJkMWRhMzA0ZDc2NGNmZWUzYTJhZTVjZDBlNGY2ZjgyN2IiLCJ0eXAiOiJKV1QifQ
eyJhbGciOiJSUzI1NiIsImtpZCI6IjFkMmE2YTZhNDcyYWNhNjNmM2FmNzU2NjIxZjM0Njg2OTI1YjUxYTgiLCJ0eXAiOiJKV1QifQ
"""
