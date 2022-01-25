from django.test import TestCase
from stage_api.models import Stage
from world_api.models import World


class StageModelsTests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される

        w1 = World.objects.create(
            name="World1",
            description="This is descriptions of world1.",
            movie_url="http://hoge.com/hogehoge",
            index=10,
        )

        w2 = World.objects.create(
            name="World1",
            description="This is descriptions of world1.",
            movie_url="http://hoge.com/hogehoge",
            index=1,
        )
        Stage.objects.create(
            stage_index=10,
            objective="This is rules of stage1.",
            movie_url="http://hoge.com/hogehoge",
            w_id=w1,
        )
        Stage.objects.create(
            stage_index=1,
            objective="ステージ２のルールです．",
            movie_url="http://world.com/worldworld",
            w_id=w2,
        )

    def test_noraml_can_speak(self):
        """正常系テスト"""
        test1 = Stage.objects.get(stage_index="10")
        w1_get = World.objects.get(index="10")
        self.assertEquals(test1.stage_index, 10)
        self.assertEquals(test1.objective, "This is rules of stage1.")
        self.assertEquals(test1.movie_url, "http://hoge.com/hogehoge")
        self.assertEquals(test1.w_id, w1_get)

    def test_animals_can_speak(self):
        """正常系テスト"""
        test2 = Stage.objects.get(stage_index="1")
        w2_get = World.objects.get(index="1")
        self.assertEquals(test2.stage_index, 1)
        self.assertEquals(test2.objective, "ステージ２のルールです．")
        self.assertEquals(test2.movie_url, "http://world.com/worldworld")
        self.assertEquals(test2.w_id, w2_get)
