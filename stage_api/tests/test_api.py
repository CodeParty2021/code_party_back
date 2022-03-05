from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from world_api.models import World
import json

from users.models import User


class StageAPITests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        # クライアント作成(TODO:ログイン必須になった場合，修正が必要)
        self.client = APIClient(enforce_csrf_checks=True)

        self.user1 = User.objects.create(
            id="fawe;ojifa;woef",
            display_name="hello",
            email="feaw@fawe.com",
            picture="http://localhost:8000/users/auth",
            is_stuff=True,
        )
        # ユーザ強制ログイン
        self.client.force_authenticate(user=self.user1)

        world1 = World.objects.create(
            name="World1",
            description="This is descriptions of world1.",
            movie_url="http://hoge.com/hogehoge",
            index=10,
        )
        world2 = World.objects.create(
            name="World1",
            description="This is descriptions of world1.",
            movie_url="http://hoge.com/hogehoge",
            index=1,
        )
        # データ準備
        self.client.post(
            "/stages/",
            {
                "index": 10,
                "objective": "This is rules of stage1.",
                "movieUrl": "http://hoge.com/hogehoge",
                "world": world1.id,
            },
            format="json",
        )
        self.client.post(
            "/stages/",
            {
                "index": 1,
                "objective": "ステージ２のルールです．",
                "movieUrl": "http://world.com/worldworld",
                "world": world2.id,
            },
            format="json",
        )

        # ログアウト
        self.client.logout()

    def test_get_list_of_all_stages(self):  # testメソッドはtest_から始めること
        """全ステージのリストを取得"""
        # GET
        world1_get = World.objects.get(index="10")
        world2_get = World.objects.get(index="1")
        response = self.client.get("/stages/", format="json")
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
                    "index": 10,
                    "objective": "This is rules of stage1.",
                    "movieUrl": "http://hoge.com/hogehoge",
                    "world": world1_get.id,
                },
                {
                    "id": 2,
                    "index": 1,
                    "objective": "ステージ２のルールです．",
                    "movieUrl": "http://world.com/worldworld",
                    "world": world2_get.id,
                },
            ],
        )

    def test_get_one_stage(self):
        """ID=1のステージを取得"""
        # GET
        world1_get = World.objects.get(index="10")
        # ユーザ強制ログイン
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/stages/1/", format="json")

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
                "index": 10,
                "objective": "This is rules of stage1.",
                "movieUrl": "http://hoge.com/hogehoge",
                "world": world1_get.id,
            },
        )

    def test_getfiltered_examples_with_a_field(self):
        """フィルターでstage_idをソートして取得"""
        # GET
        world1_get = World.objects.get(index="10")
        world2_get = World.objects.get(index="1")
        response = self.client.get("/stages/", {"order_by": "index"}, format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                {
                    "id": 2,
                    "index": 1,
                    "objective": "ステージ２のルールです．",
                    "movieUrl": "http://world.com/worldworld",
                    "world": world2_get.id,
                },
                {
                    "id": 1,
                    "index": 10,
                    "objective": "This is rules of stage1.",
                    "movieUrl": "http://hoge.com/hogehoge",
                    "world": world1_get.id,
                },
            ],
        )

    def test_getfiltered_examples_index(self):
        """indexが一致するものだけを取得"""
        # GET
        world2_get = World.objects.get(index="1")
        response = self.client.get("/stages/", {"index": 1}, format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                {
                    "id": 2,
                    "index": 1,
                    "objective": "ステージ２のルールです．",
                    "movieUrl": "http://world.com/worldworld",
                    "world": world2_get.id,
                }
            ],
        )

    def test_getfiltered_examples_world_id(self):
        """worldのidが一致するものだけを取得"""
        # GET
        world1_get = World.objects.get(index="10")
        response = self.client.get("/stages/", {"world": world1_get.id}, format="json")
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
                    "index": 10,
                    "objective": "This is rules of stage1.",
                    "movieUrl": "http://hoge.com/hogehoge",
                    "world": world1_get.id,
                }
            ],
        )
