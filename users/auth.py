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
            display_name = decoded_token.get("name", "名無しオペレータ")
            email = decoded_token.get("email", None)
            picture = decoded_token.get("picture", None)

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
