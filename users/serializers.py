from rest_framework import serializers
from .models import User
from firebase_admin import auth


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # 利用するモデル
        model = User

        # モデルのfiled以外で受け取るもの
        extra_kwargs = {"idToken": {"write_only": True}}
        fields = ("displayName", "photo_url")
        # モデルのfiledだが受け取りたくないもの
        exclude = ["id"]

    # デシリアライズ時のオブジェクト生成メソッド, validated_dateに中身が入っている
    def create(self, validated_data):
        id_token = validated_data.idToken

        # firebaseでのtoken検証
        # https://firebase.google.com/docs/auth/admin/verify-id-tokens?hl=ja
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        user, created = User.objects.update_or_create(
            id=uid,
            display_name=validated_data["display_name"],
            photo_url=validated_data["photo_url"],
        )  # created でcreateされたのならtrue,そうでなければfalseが返ってくる
        return {"user": user, "created": created}  # ここのレスポンスが答えになる
