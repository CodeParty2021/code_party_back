from django.test import TestCase
from step_api.models import Step
from stage_api.models import Stage
from world_api.models import World


class StepModelsTests(TestCase):
    def setUp(self):

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
        Step.objects.create(
            objective="達成条件はXXです",
            description="このステップではXXXします",
            index=10,
            stage=stage1,
        )

        Step.objects.create(
            objective="達成条件はZZZです",
            description="このステップではYYYします",
            index=20,
            stage=stage2,
        )

    def test_noraml_can_speak(self):
        """正常系テスト"""
        test1 = Step.objects.get(index="10")
        stage_get = Stage.objects.get(index="10")
        self.assertEquals(test1.objective, "達成条件はXXです")
        self.assertEquals(test1.description, "このステップではXXXします")
        self.assertEquals(test1.index, 10)
        self.assertEquals(test1.stage, stage_get)

    def test_animals_can_speak(self):
        """正常系テスト"""
        test1 = Step.objects.get(index="20")
        stage_get = Stage.objects.get(index="1")
        self.assertEquals(test1.objective, "達成条件はZZZです")
        self.assertEquals(test1.description, "このステップではYYYします")
        self.assertEquals(test1.index, 20)
        self.assertEquals(test1.stage, stage_get)
