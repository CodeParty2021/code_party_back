from django.test import TestCase

from world_api.models import World
from stage_api.models import Stage
from step_api.models import Step
from code_api.models import Code, ProgrammingLanguage
from result_api.models import Result
from users.models import User


class ResultModelsTests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
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
        )
        result1.codes.set([self.code1, self.code2, self.code3])

        result2 = Result.objects.create(
            json_path="/result/0002.json",
            step=self.step,
        )
        result2.codes.set([self.code2, self.code3, self.code4])

        self.test_id1 = result1.id
        self.test_id2 = result2.id

    def test_model_get_code1(self):
        """正常系テスト"""
        test1 = Result.objects.get(id=self.test_id1)
        # 色々チェック
        self.assertEquals(test1.json_path, "/result/0001.json")
        self.assertEquals(test1.step, self.step)
        codes = list(test1.codes.all())
        self.assertEquals(self.code1 in codes, True)
        self.assertEquals(self.code2 in codes, True)
        self.assertEquals(self.code3 in codes, True)
        self.assertEquals(self.code4 in codes, False)

    def test_model_get_code2(self):
        """正常系テスト"""
        test2 = Result.objects.get(id=self.test_id2)
        # 色々チェック
        self.assertEquals(test2.json_path, "/result/0002.json")
        self.assertEquals(test2.step, self.step)
        codes = list(test2.codes.all())
        self.assertEquals(self.code1 in codes, False)
        self.assertEquals(self.code2 in codes, True)
        self.assertEquals(self.code3 in codes, True)
        self.assertEquals(self.code4 in codes, True)
