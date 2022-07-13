from django.test import TestCase
from world_api.models import World
from stage_api.models import Stage
from step_api.models import Step
from code_api.models import Code, ProgrammingLanguage
from users.models import User


class CodeModelsTests(TestCase):
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
        self.lang_javascript = ProgrammingLanguage.objects.create(name="JavaScript")
        self.user = User.objects.create(
            id="fawe;ojifa;woef",
            display_name="hello",
            email="feaw@fawe.com",
            picture="http://localhost:8000/users/auth",
        )

        # Codeの生成
        code1 = Code.objects.create(
            code_content="print('hello world!')",
            language=self.lang_python,
            step=self.step,
            user=self.user,
        )
        code2 = Code.objects.create(
            code_content="Alert('hello world!')",
            language=self.lang_javascript,
            step=self.step,
            user=self.user,
        )

        # idの記録
        self.test_id1 = code1.id
        self.test_id2 = code2.id

    def test_model_get_code1(self):
        """正常系テスト"""
        test1 = Code.objects.get(id=self.test_id1)
        # 色々チェック
        self.assertEquals(test1.code_content, "print('hello world!')")
        self.assertEquals(test1.language, self.lang_python)
        self.assertEquals(test1.step, self.step)
        self.assertEquals(test1.user, self.user)

    def test_model_get_code2(self):
        """正常系テスト"""
        test2 = Code.objects.get(id=self.test_id2)
        # 色々チェック
        self.assertEquals(test2.code_content, "Alert('hello world!')")
        self.assertEquals(test2.language, self.lang_javascript)
        self.assertEquals(test2.step, self.step)
        self.assertEquals(test2.user, self.user)
