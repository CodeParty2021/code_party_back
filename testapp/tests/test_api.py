from django.test import TestCase
from testapp.models import TestModel
from django.test.client import Client
import json


class TestModelAPITests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        TestModel.objects.create(name="テスト1", age=23)
        TestModel.objects.create(name="テスト2", age=22)

    def test_noraml_can_speak(self):
        """正常系テスト"""
        client = Client()
        response = client.get("/api/testmodels/")
        self.assertEquals(response.status_code, 200)
        body = json.loads(response.content.decode("utf-8"))
        self.assertEquals(
            body, [{"name": "テスト1", "age": 23}, {"name": "テスト2", "age": 22}]
        )
