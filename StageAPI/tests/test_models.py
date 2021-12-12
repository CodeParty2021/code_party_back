from django.test import TestCase
from StageAPI.models import Stage


class StageModelsTests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        Stage.objects.create(name="Stage1", stage_index=10, rule="This is rules of stage1.")
        Stage.objects.create(name="ステージ2", stage_index=1, rule="ステージ２のルールです．")

    def test_noraml_can_speak(self):
        """正常系テスト"""
        test1 = Stage.objects.get(name="Stage1")
        self.assertEquals(test1.name, "Stage1")
        self.assertEquals(test1.stage_index, 10)
        self.assertEquals(test1.rule, "This is rules of stage1.")

    def test_animals_can_speak(self):
        """正常系テスト"""
        test2 = Stage.objects.get(name="ステージ2")
        self.assertEquals(test2.name, "ステージ2")
        self.assertEquals(test2.stage_index, 1)
        self.assertEquals(test2.rule, "ステージ２のルールです．")
