from django.test import TestCase

# Create your tests here.
from code_party_back.testapp.models import TestModel


class TestModelTests(TestCase):
    def setUp(self): # テストケース実行毎に実行される
        TestModel.objects.create(name="テスト1", age=23)
        TestModel.objects.create(name="テスト2", age=22)

    def test_animals_can_speak(self):
        """正常系テスト"""
        test1 = TestModel.objects.get(name="テスト1")
        self.assertEquals(test1.name, "テスト1")
        self.assertEquals(test1.age, 23)