from django.test import TestCase

# Create your tests here.
from testapp.models import TestModel


class TestModelModelsTests(TestCase):
    def setUp(self): # テストケース実行毎に実行される
        TestModel.objects.create(name="テスト1", age=23)
        TestModel.objects.create(name="テスト2", age=22)

    def test_noraml_can_speak(self):
        """正常系テスト"""
        test1 = TestModel.objects.get(name="テスト1")
        self.assertEquals(test1.name, "テスト1")
        self.assertEquals(test1.age, 23)


    def test_animals_can_speak(self):
        """正常系テスト"""
        test2 = TestModel.objects.get(name="テスト2")
        self.assertEquals(test2.name, "テスト2")
        self.assertEquals(test2.age, 22)