from urllib import response
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from stage_api.models import Stage
import json


class StageAPITests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        # クライアント作成(TODO:ログイン必須になった場合，修正が必要)
        self.client = APIClient(enforce_csrf_checks=True)
        # データ準備
        self.client.post(
            "/stages/",
            {"name": "Stage1", "stageIndex": 10, "rule": "This is rules of stage1."},
            format="json",
        )
        self.client.post(
            "/stages/",
            {"name": "ステージ２", "stageIndex": 1, "rule": "ステージ２のルールです．"},
            format="json",
        )

    def test_get_list_of_all_stages(self):  # testメソッドはtest_から始めること
        """全ステージのリストを取得"""
        # GET
        response = self.client.get("/stages/", format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                {
                    "id": 1,
                    "name": "Stage1",
                    "stageIndex": 10,
                    "rule": "This is rules of stage1.",
                },
                {"id": 2, "name": "ステージ２", "stageIndex": 1, "rule": "ステージ２のルールです．"},
            ],
        )

    def test_get_one_stage(self):
        """ID=1のステージを取得"""
        # GET
        response = self.client.get("/stages/1/", format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            {
                "id": 1,
                "name": "Stage1",
                "stageIndex": 10,
                "rule": "This is rules of stage1.",
            },
        )

    def test_getfiltered_examples_with_a_field(self):
        """name=Stage でフィルターしてステージをソートして取得"""
        #GET
        response = self.client.get("/stages/", {
            "name":"Stage",
            "order_by": "stage_index"
        }, format ="json")
        #レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code,200)
        #jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        #データチェック
        self.assertEquals(
            body,
            [
                {
                    'id': 2,
                    'name': 'ステージ２',
                    'stageIndex': 1,
                    'rule': 'ステージ２のルールです．'
                },
                {
                    'id': 1,
                    'name': 'Stage1',
                    'stageIndex': 10,
                    'rule': 'This is rules of stage1.'
                },   
            ]
        )

