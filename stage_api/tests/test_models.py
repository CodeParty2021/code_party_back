from django.test import TestCase
from stage_api.models import Stage


class StageModelsTests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        Stage.objects.create(
            stage_index=10, objective="This is rules of stage1.",movie_url="http://hoge.com/hogehoge",
        )
        Stage.objects.create(stage_index=1, objective="ステージ２のルールです．",movie_url="http://world.com/worldworld")

    def test_noraml_can_speak(self):
        """正常系テスト"""
        test1 = Stage.objects.get(stage_index="10")
        self.assertEquals(test1.stage_index, 10)
        self.assertEquals(test1.objective, "This is rules of stage1.")
        self.assertEquals(test1.movie_url, "http://hoge.com/hogehoge")

    def test_animals_can_speak(self):
        """正常系テスト"""
        test2 = Stage.objects.get(stage_index="1")
        self.assertEquals(test2.stage_index, 1)
        self.assertEquals(test2.objective, "ステージ２のルールです．")
        self.assertEquals(test2.movie_url, "http://world.com/worldworld")
