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
        stage1 = self.client.post(
            "/stages/",
            {
                "index": 10,
                "objective": "This is rules of stage1.",
                "movieUrl": "http://hoge.com/hogehoge",
                "world": world1.id,
            },
            format="json",
        )
        stage2 = self.client.post(
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

        # idとタイムスタンプの記録
        stage1 = json.loads(stage1.content.decode("utf-8"))
        stage2 = json.loads(stage2.content.decode("utf-8"))

        self.test_id1 = stage1["id"]
        self.test_id2 = stage2["id"]

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

    def test_update_invalid_user(self):
        """stuff以外が編集しようとした時にアクセスを拒否する"""
        # ユーザ1としてログイン
        self.client.force_authenticate(user=self.user1)
        # ステージ1の編集
        stage_edit_user = self.client.patch(
            f"/stages/1/",
            {"name": "print('update!')"},
            format="json",
        )

        # ログアウト
        self.client.logout()
    
        # ユーザ2としてログイン
        self.client.force_authenticate(user=self.user2)
        stage_view = self.client.get(f"/stages/1/", format="json")
        # データ3の編集
        stage_edit_no_stuff = self.client.patch(
            f"/stages/1/",
            {"name": "print('update2!')"},
            format="json",
        )
        # データ3の削除
        stage_delete_no_stuff = self.client.delete(f"/stages/1/", format="json")

        # データチェック
        self.assertEquals(stage_edit_user.status_code, 200)  # Staffなので編集OK
        self.assertEquals(stage_view.status_code, 200)  # Staffではないが閲覧だけなのでOK
        self.assertEquals(stage_edit_no_stuff.status_code, 403)  # Staffじゃないので編集できない
        self.assertEquals(stage_delete_no_stuff.status_code, 403)  # Staffじゃないので削除できない
