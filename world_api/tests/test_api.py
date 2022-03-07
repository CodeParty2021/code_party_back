from django.test import TestCase
from rest_framework.test import APIClient
import json

from users.models import User


class WorldAPITests(TestCase):
    def setUp(self):
        # クライアント作成(TODO:ログイン必須になった場合，修正が必要)
        self.client = APIClient(enforce_csrf_checks=True)

        self.user1 = User.objects.create(
            id="fawe;ojifa;woef",
            display_name="hello",
            email="feaw@fawe.com",
            picture="http://localhost:8000/users/auth",
            is_staff=True,
        )

        self.user2 = User.objects.create(
            id="fawe;oasdfa;woef",
            display_name="hello_user2",
            email="feawaaaaa@fawe.com",
            picture="http://localhost:8000/users/auth",
        )
        # ユーザ強制ログイン
        self.client.force_authenticate(user=self.user1)
        # データ準備
        self.client.post(
            "/worlds/",
            {
                "name": "World1",
                "description": "This is descriptions of world1.",
                "movie_url": "http://hoge.com/hogehoge",
                "index": 10,
            },
            format="json",
        )
        self.client.post(
            "/worlds/",
            {
                "name": "ワールド3",
                "description": "ワールド３の説明です．",
                "movie_url": "http://world3.com/",
                "index": 2,
            },
            format="json",
        )
        self.client.post(
            "/worlds/",
            {
                "name": "ワールド2",
                "description": "ワールド２の説明です．",
                "movie_url": "http://world.com/worldworld",
                "index": 1,
            },
            format="json",
        )

        # ログアウト
        self.client.logout()

    def test_get_list_of_all_worlds(self):
        """全ワールドのリストを取得"""
        # GET
        response = self.client.get("/worlds/", format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                {
                    "id": 1,
                    "name": "World1",
                    "description": "This is descriptions of world1.",
                    "movieUrl": "http://hoge.com/hogehoge",
                    "index": 10,
                },
                {
                    "id": 2,
                    "name": "ワールド3",
                    "description": "ワールド３の説明です．",
                    "movieUrl": "http://world3.com/",
                    "index": 2,
                },
                {
                    "id": 3,
                    "name": "ワールド2",
                    "description": "ワールド２の説明です．",
                    "movieUrl": "http://world.com/worldworld",
                    "index": 1,
                },
            ],
        )

    def test_get_one_world(self):
        """ID=1のワールドを取得"""
        # ユーザ強制ログイン
        self.client.force_authenticate(user=self.user1)
        # GET
        response = self.client.get("/worlds/1/", format="json")
        # ログアウト
        self.client.logout()
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            {
                "id": 1,
                "name": "World1",
                "description": "This is descriptions of world1.",
                "movieUrl": "http://hoge.com/hogehoge",
                "index": 10,
            },
        )

    def test_get_filtered_worlds_with_name(self):
        """name=ワールド でフィルターしてワールドをソートして取得"""
        # GET
        response = self.client.get(
            "/worlds/", {"name": "ワールド", "order_by": "index"}, format="json"
        )
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                {
                    "id": 3,
                    "name": "ワールド2",
                    "description": "ワールド２の説明です．",
                    "movieUrl": "http://world.com/worldworld",
                    "index": 1,
                },
                {
                    "id": 2,
                    "name": "ワールド3",
                    "description": "ワールド３の説明です．",
                    "movieUrl": "http://world3.com/",
                    "index": 2,
                },
            ],
        )

    def test_update_invalid_user(self):
        """staff以外が編集しようとした時にアクセスを拒否する"""
        # ユーザ1としてログイン
        self.client.force_authenticate(user=self.user1)
        # ステージ1の編集
        world_edit_user = self.client.patch(
            f"/worlds/1/",
            {"objective": "print('update!')"},
            format="json",
        )

        # ログアウト
        self.client.logout()

        # ユーザ2としてログイン
        self.client.force_authenticate(user=self.user2)
        world_view = self.client.get(f"/worlds/1/", format="json")
        # データ3の編集
        world_edit_no_stuff = self.client.patch(
            f"/worlds/1/",
            {"name": "print('update2!')"},
            format="json",
        )
        # データ3の削除
        world_delete_no_stuff = self.client.delete(f"/worlds/1/", format="json")

        # データチェック
        self.assertEquals(world_edit_user.status_code, 200)  # Staffなので編集OK
        self.assertEquals(world_view.status_code, 200)  # Staffではないが閲覧だけなのでOK
        self.assertEquals(world_edit_no_stuff.status_code, 403)  # Staffじゃないので編集できない
        self.assertEquals(world_delete_no_stuff.status_code, 403)  # Staffじゃないので削除できない
