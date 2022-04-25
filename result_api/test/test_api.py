import json
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from world_api.models import World
from stage_api.models import Stage
from step_api.models import Step
from code_api.models import Code, ProgrammingLanguage
from result_api.models import Result
from users.models import User


class ResultAPITests(TestCase):
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
        self.step1 = Step.objects.create(
            objective="This is objectives of this step1.",
            description="This is descriptions of this step1.",
            index=3,
            stage=stage,
        )
        self.step2 = Step.objects.create(
            objective="This is objectives of this step2.",
            description="This is descriptions of this step2.",
            index=2,
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
            code_content="def select(a,b,c):\n return 1",
            language=self.lang_python,
            step=self.step1,
            user=self.user,
        )
        self.code2 = Code.objects.create(
            code_content="def select(a,b,c):\n return 1",
            language=self.lang_python,
            step=self.step1,
            user=self.user,
        )
        self.code3 = Code.objects.create(
            code_content="def select(a,b,c):\n return 1",
            language=self.lang_python,
            step=self.step2,
            user=self.user,
        )
        self.code4 = Code.objects.create(
            code_content="def select(a,b,c):\n return 1",
            language=self.lang_python,
            step=self.step2,
            user=self.user,
        )

        # resultの生成
        result1 = Result.objects.create(
            json_path="/result/0001.json",
            step=self.step1,
        )
        result1.codes.add(self.code1)
        result1.codes.add(self.code2)
        result1.codes.add(self.code3)

        result2 = Result.objects.create(
            json_path="/result/0002.json",
            step=self.step2,
        )
        result2.codes.add(self.code2)
        result2.codes.add(self.code3)
        result2.codes.add(self.code4)

        # idの記録
        self.test_id1 = result1.id.urn[9:]
        self.test_id2 = result2.id.urn[9:]

        # 想定データを作成
        self.res_data1 = {
            "id": self.test_id1,
            "jsonPath": "/result/0001.json",
            "createdAt": timezone.localtime(result1.created_at).isoformat(),
            "step": self.step1.id,
            "codes": [code.id.urn[9:] for code in result1.codes.all()],
        }
        self.res_data2 = {
            "id": self.test_id2,
            "jsonPath": "/result/0002.json",
            "createdAt": timezone.localtime(result2.created_at).isoformat(),
            "step": self.step2.id,
            "codes": [code.id.urn[9:] for code in result2.codes.all()],
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
        response = self.client.get(f"/results/{self.test_id1}/", format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(body, self.res_data1)

    def test_get_filtered_results_with_step(self):
        """step.idでフィルターして取得"""
        # GET
        response = self.client.get("/results/", {"step": self.step1.id}, format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                self.res_data1,
            ],
        )

    def test_get_filtered_results_with_code(self):
        """code.idでフィルターして取得"""
        # GET
        response = self.client.get(
            "/results/", {"codes": self.code4.id.urn[9:]}, format="json"
        )
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                self.res_data2,
            ],
        )

    def test_get_ordered_by_created_at(self):
        """created_atでソートして取得"""
        # GET
        response = self.client.get(
            "/results/", {"order_by": "-created_at"}, format="json"
        )
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                self.res_data2,
                self.res_data1,
            ],
        )

    def test_run_code_and_get_result(self):
        """code/:id/runを実行し，resultのjsonを取得する"""
        # テストデータが足りないのでデータを追加
        Code.objects.create(
            code_content="def select(a,b,c):\n return 1",
            language=self.lang_python,
            step=self.step1,
            user=self.user,
        )
        Code.objects.create(
            code_content="def select(a,b,c):\n return 1",
            language=self.lang_python,
            step=self.step1,
            user=self.user,
        )

        # code/:id/runを実行
        response1 = self.client.post(
            f"/codes/run/", {"code": [self.code1.id.urn[9:], self.code2.id.urn[9:]]}
        )
        # レスポンスのステータスコードをチェック
        self.assertEquals(response1.status_code, 200)
        # jsonをデコード
        body = json.loads(response1.content.decode("utf-8"))
        # ID取得
        result_id = body["jsonId"]
        # resultAPIからjsonを取得
        response2 = self.client.get(f"/results/{result_id}/json/")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response2.status_code, 200)
