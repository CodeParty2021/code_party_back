import json
from django.test import TestCase
from rest_framework.test import APIClient

from world_api.models import World
from stage_api.models import Stage
from step_api.models import Step
from code_api.models import ProgrammingLanguage
from users.models import User


class StageAPITests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        # クライアント作成(TODO:ログイン必須になった場合，修正が必要)
        self.client = APIClient(enforce_csrf_checks=True)

        #Step, Userの作成
        world = World.objects.create(
            name="World",
            description="This is descriptions of this world.",
            movie_url="http://hoge.com/hogehoge",
            index=10,
        )
        stage = Stage.objects.create(
            index=5,
            objective="This is rules of this stage.",
            movie_url="http://hoge.com/hogehoge",
            world=world,
        )
        self.step1 = Step.objects.create(
            objective="This is objectives of this step1.",
            description="This is descriptions of this step1.",
            index=3,
            stage=stage,
        )
        self.step2 = Step.objects.create(
            objective="This is objectives of this step2.",
            description="This is descriptions of this step2.",
            index=5,
            stage=stage,
        )
        self.lang_python = ProgrammingLanguage.objects.create(
            name = "Python"
        )
        self.lang_javascript = ProgrammingLanguage.objects.create(
            name = "JavaScript"
        )

        # 一人目のユーザ
        self.user1 = User.objects.create(
            id="fawe;ojifa;woef",
            display_name="hello",
            email="feaw@fawe.com",
            picture="http://localhost:8000/users/auth",
        )

        # ユーザ強制ログイン
        self.client.force_authenticate(user=self.user1)

        # データ準備
        data1 = self.client.post(
            "/codes/",
            {
                "code_content" : "print('hello world!')",
                "language" : self.lang_python.id,
                "step" : self.step1.id
            },
            format="json",
        )
        data2 = self.client.post(
            "/codes/",
            {
                "code_content" : "Alert('hello world!')",
                "language" : self.lang_javascript.id,
                "step" : self.step2.id
             },
            format="json",
        )

        # 二人目のユーザ
        self.user2 = User.objects.create(
            id="aksjdfj;a;sdkfj;",
            display_name="test user 2",
            email="sadwer@asdjkfk.com",
            picture="http://localhost:8000/",
        )

        # ユーザ強制ログイン
        self.client.force_authenticate(user=self.user2)

        data3 = self.client.post(
            "/codes/",
            {
                "code_content" : "pass",
                "language" : self.lang_python.id,
                "step" : self.step1.id
             },
            format="json",
        )

        # ログアウト
        self.client.logout()

        # idとタイムスタンプの記録
        data1 = json.loads(data1.content.decode("utf-8"))
        data2 = json.loads(data2.content.decode("utf-8"))
        data3 = json.loads(data3.content.decode("utf-8"))

        self.test_id1 = data1.id
        self.test_id2 = data2.id
        self.test_id3 = data3.id

        # 想定データを作成
        self.res_data1 = {
            "id" : self.test_id1,
            "codeContent" : "print('hello world!')",
            "language" : self.lang_python.id,
            "step" : self.step1.id,
            "user" : self.user1.id,
            "updated_at" : data1.updated_at,
            "created_at" : data1.created_at,
        }
        self.res_data2 = {
            "id" : self.test_id2,
            "codeContent" : "Alert('hello world!')",
            "language" : self.lang_javascript.id,
            "step" : self.step2.id,
            "user" : self.user1.id,
            "updated_at" : data2.updated_at,
            "created_at" : data2.created_at,
        }
        self.res_data3 = {
            "id" : self.test_id3,
            "codeContent" : "pass",
            "language" : self.lang_python.id,
            "step" : self.step2.id,
            "user" : self.user2.id,
            "updated_at" : data3.updated_at,
            "created_at" : data3.created_at,
        }

    def test_get_list_of_all_codes(self):
        """全コードのリストを取得"""
        # GET
        response = self.client.get("/codes/", format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                self.res_data1,
                self.res_data2,
                self.res_data3,
            ],
        )

    def test_get_one_code(self):
        """ID=self.test_id1のステージを取得"""
        # GET
        response = self.client.get(f"/codes/{self.test_id1}/", format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(body, self.res_data1)

    def test_get_filtered_codes_with_language(self):
        """language.idでフィルターして取得"""
        #GET
        response = self.client.get("/codes/", {
            "language": self.lang_python.id
        }, format ="json")
        #レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        #jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        #データチェック
        self.assertEquals(
            body,
            [
                self.res_data1,
                self.res_data3,
            ]
        )

    def test_get_filtered_codes_with_step(self):
        """step.idでフィルターして取得"""
        #GET
        response = self.client.get("/codes/", {
            "step": self.step1.id
        }, format ="json")
        #レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        #jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        #データチェック
        self.assertEquals(
            body,
            [
                self.res_data2,
                self.res_data3,
            ]
        )

    def test_get_filtered_codes_with_user(self):
        """user.idでフィルターして取得"""
        #GET
        response = self.client.get("/codes/", {
            "user": self.user1.id
        }, format ="json")
        #レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        #jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        #データチェック
        self.assertEquals(
            body,
            [
                self.res_data1,
                self.res_data2,
            ]
        )

    def test_get_ordered_by_created_at(self):
        """created_atでソートして取得"""
        #GET
        response = self.client.get("/codes/", {
          "order_by" : "-created_at"
        },format ="json")
        #レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code,200)
        #jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                self.res_data3,
                self.res_data2,
                self.res_data1,
            ],
        )

    def test_get_ordered_by_updated_at(self):
        """updated_atでソートして取得"""
        #一件だけ更新
        self.client.post(
            f"/codes/{self.test_id1}/",
            {
                "code_content" : "print('update!')"
            },
            format="json",
        )
        #GET
        response = self.client.get("/codes/", {
          "order_by" : "-updated_at"
        },format ="json")
        #レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code,200)
        #jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                {**self.res_data1, "codeContent" : "print('update!')"},
                self.res_data3,
                self.res_data2,
            ],
        )