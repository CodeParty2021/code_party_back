from django.test import TestCase
from world_api.models import World


class WorldModelsTests(TestCase):
    def setUp(self):
        World.objects.create(
            name="World1",
            description="This is descriptions of world1.",
            movie_url="http://hoge.com/hogehoge",
            index=10,
        )
        World.objects.create(
            name="ワールド2",
            description="ワールド２の説明です．",
            movie_url="http://world.com/worldworld",
            index=1,
        )

    def test_noraml_can_speak(self):
        """正常系テスト"""
        test1 = World.objects.get(name="World1")
        self.assertEquals(test1.name, "World1")
        self.assertEquals(test1.description, "This is descriptions of world1.")
        self.assertEquals(test1.movie_url, "http://hoge.com/hogehoge")
        self.assertEquals(test1.index, 10)

    def test_animals_can_speak(self):
        """正常系テスト"""
        test2 = World.objects.get(name="ワールド2")
        self.assertEquals(test2.name, "ワールド2")
        self.assertEquals(test2.description, "ワールド２の説明です．")
        self.assertEquals(test2.movie_url, "http://world.com/worldworld")
        self.assertEquals(test2.index, 1)
