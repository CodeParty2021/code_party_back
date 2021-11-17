from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from api.models import Stage
from django.test.client import Client
import json


class StageAPITests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        factory = APIRequestFactory(enforce_csrf_checks=True)
        factory.post('/api/stages/', {'name': 'Stage1', 'stage_index': 10, 'rule': 'This is rules of stage1.'}, format='json')
        response = factory.post('/api/stages/', {'name': 'ステージ２', 'stage_index': 1, 'rule': 'ステージ２のルールです．'}, format='json')
        print(response.__dict__)

    def test_get_list_of_all_stages(self):
        """正常系テスト"""
        client = APIClient(enforce_csrf_checks=True)
        response = client.get("/api/stages/?format=json")
        print(response.content)
        self.assertEquals(response.status_code, 200)
        body = json.loads(response.content.decode("utf-8"))
        self.assertEquals(
            body, [{'name': 'Stage1', 'stage_index': 10, 'rule': 'This is rules of stage1.'}, {'name': 'ステージ２', 'stage_index': 1, 'rule': 'ステージ２のルールです．'}]
        )
