import json
from django.test import TestCase
from rest_framework.test import APIClient

from world_api.models import World
from stage_api.models import Stage
from step_api.models import Step
from code_api.models import Code, ProgrammingLanguage
from result_api.models import Result
from users.models import User


class StageAPITests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        # クライアント作成(TODO:ログイン必須になった場合，修正が必要)
        self.client = APIClient(enforce_csrf_checks=True)

        # Step, Userの作成
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
        self.step = Step.objects.create(
            objective="This is objectives of this step.",
            description="This is descriptions of this step.",
            index=3,
            stage=stage,
        )
        self.lang_python = ProgrammingLanguage.objects.create(name="Python")
        self.user = User.objects.create(
            id="fawe;ojifa;woef",
            display_name="hello",
            email="feaw@fawe.com",
            picture="http://localhost:8000/users/auth",
        )
        self.code1 = Code.objects.create(
            code_content="print('player1')",
            language=self.lang_python,
            step=self.step,
            user=self.user,
        )
        self.code2 = Code.objects.create(
            code_content="print('player2')",
            language=self.lang_python,
            step=self.step,
            user=self.user,
        )
        self.code3 = Code.objects.create(
            code_content="print('player3')",
            language=self.lang_python,
            step=self.step,
            user=self.user,
        )
        self.code4 = Code.objects.create(
            code_content="print('player4')",
            language=self.lang_python,
            step=self.step,
            user=self.user,
        )

        # resultの生成
        result1 = Result.objects.create(
            json_path="/result/0001.json",
            step=self.step,
            codes=[self.code1, self.code2, self.code3],
        )
        result2 = Result.objects.create(
            json_path="/result/0002.json",
            step=self.step,
            codes=[self.code2, self.code3, self.code4],
        )

        # idの記録
        self.test_id1 = result1.id
        self.test_id2 = result2.id

        # 想定データを作成
        self.res_data1 = {
            "id": self.test_id1,
            "jsonPath" : "/result/0001.json",
            "step" : self.step.id,
            "codes" : [self.code1.id, self.code2.id, self.code3.id,],
            "createdAt": result1["createdAt"],
        }
        self.res_data2 = {
            "id": self.test_id2,
            "jsonPath" : "/result/0002.json",
            "step" : self.step.id,
            "codes" : [self.code2.id, self.code3.id, self.code4.id,],
            "createdAt": result2["createdAt"],
        }

    def test_get_list_of_all_results(self):
        """全Resultのリストを取得"""
        # GET
        response = self.client.get("/results/", format="json")
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
            ],
        )

    def test_get_one_result(self):
        """ID=self.test_id1のResultを取得"""
        # GET
        response = self.client.get(f"/codes/{self.test_id1}/", format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(body, self.res_data1)
