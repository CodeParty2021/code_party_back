from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from world_api.models import World
from stage_api.models import Stage
import json


from users.models import User


class StepAPITests(TestCase):
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

        # データ準備
        world1 = World.objects.create(
            name="World1",
            description="This is descriptions of world1.",
            movie_url="http://hoge.com/hogehoge",
            index=10,
        )

        stage1 = Stage.objects.create(
            index=10,
            objective="This is rules of stage1.",
            movie_url="http://hoge.com/hogehoge",
            world=world1,
        )

        stage2 = Stage.objects.create(
            index=1,
            objective="This is rules of stage2.",
            movie_url="http://hoge.com/hogehoge2",
            world=world1,
        )

        self.client.post(
            "/steps/",
            {
                "objective": "達成条件はXXです",
                "description": "このステップではXXXします",
                "index": 10,
                "stage": stage1.id,
            },
            format="json",
        )
        self.client.post(
            "/steps/",
            {
                "objective": "達成条件はZZZです",
                "description": "このステップではYYYします",
                "index": 3,
                "stage": stage2.id,
            },
            format="json",
        )

        # ログアウト
        self.client.logout()

    def test_get_list_of_all_steps(self):  # testメソッドはtest_から始めること
        """全ステップのリストを取得"""
        # GET
        stage1_get = Stage.objects.get(index="10")
        stage2_get = Stage.objects.get(index="1")
        response = self.client.get("/steps/", format="json")
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
                    "objective": "達成条件はXXです",
                    "description": "このステップではXXXします",
                    "index": 10,
                    "stage": stage1_get.id,
                },
                {
                    "id": 2,
                    "objective": "達成条件はZZZです",
                    "description": "このステップではYYYします",
                    "index": 3,
                    "stage": stage2_get.id,
                },
            ],
        )

    def test_get_one_step(self):
        """ID=1のステップを取得"""
        # ユーザ強制ログイン
        self.client.force_authenticate(user=self.user1)
        # GET
        stage1_get = Stage.objects.get(index="10")

        response = self.client.get("/steps/1/", format="json")

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
                "objective": "達成条件はXXです",
                "description": "このステップではXXXします",
                "index": 10,
                "stage": stage1_get.id,
            },
        )

    def test_getfiltered_examples_with_a_field(self):
        """フィルターでstep_indexをソートして取得"""
        # GET
        stage1_get = Stage.objects.get(index="10")
        stage2_get = Stage.objects.get(index="1")
        response = self.client.get("/steps/", {"order_by": "index"}, format="json")
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
                    "objective": "達成条件はZZZです",
                    "description": "このステップではYYYします",
                    "index": 3,
                    "stage": stage2_get.id,
                },
                {
                    "id": 1,
                    "objective": "達成条件はXXです",
                    "description": "このステップではXXXします",
                    "index": 10,
                    "stage": stage1_get.id,
                },
            ],
        )

    def test_getfiltered_examples_index(self):
        """indexが一致するものだけを取得"""
        # GET
        stage2_get = Stage.objects.get(index="1")
        response = self.client.get("/steps/", {"index": 3}, format="json")
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
                    "objective": "達成条件はZZZです",
                    "description": "このステップではYYYします",
                    "index": 3,
                    "stage": stage2_get.id,
                }
            ],
        )

    def test_getfiltered_examples_stage_id(self):
        """stageのidが一致するものだけを取得"""
        # GET
        stage1_get = Stage.objects.get(index="10")
        response = self.client.get("/steps/", {"stage": stage1_get.id}, format="json")
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
                    "objective": "達成条件はXXです",
                    "description": "このステップではXXXします",
                    "index": 10,
                    "stage": stage1_get.id,
                }
            ],
        )

    def test_update_invalid_user(self):
        """staff以外が編集しようとした時にアクセスを拒否する"""
        # ユーザ1としてログイン
        self.client.force_authenticate(user=self.user1)
        # ステージ1の編集
        step_edit_user = self.client.patch(
            f"/steps/1/",
            {"objective": "print('update!')"},
            format="json",
        )

        # ログアウト
        self.client.logout()
    
        # ユーザ2としてログイン
        self.client.force_authenticate(user=self.user2)
        step_view = self.client.get(f"/steps/1/", format="json")
        # データ3の編集
        step_edit_no_stuff = self.client.patch(
            f"/steps/1/",
            {"name": "print('update2!')"},
            format="json",
        )
        # データ3の削除
        step_delete_no_stuff = self.client.delete(f"/steps/1/", format="json")

        # データチェック
        self.assertEquals(step_edit_user.status_code, 200)  # Staffなので編集OK
        self.assertEquals(step_view.status_code, 200)  # Staffではないが閲覧だけなのでOK
        self.assertEquals(step_edit_no_stuff.status_code, 403)  # Staffじゃないので編集できない
        self.assertEquals(step_delete_no_stuff.status_code, 403)  # Staffじゃないので削除できない
