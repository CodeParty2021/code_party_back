from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from StageAPI.models import Stage
import json


class StageAPITests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        # クライアント作成(TODO:ログイン必須になった場合，修正が必要)
        self.client = APIClient(enforce_csrf_checks=True)
        # データ準備
        self.client.post(
            "/stageapi/stages/",
            {"name": "Stage1", "stage_index": 10, "rule": "This is rules of stage1."},
            format="json",
        )
        self.client.post(
            "/stageapi/stages/",
            {"name": "ステージ２", "stage_index": 1, "rule": "ステージ２のルールです．"},
            format="json",
        )

    def test_get_list_of_all_stages(self):
        """全ステージのリストを取得"""
        # GET
        response = self.client.get("/stageapi/stages/", format="json")
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
                    "stage_index": 10,
                    "rule": "This is rules of stage1.",
                },
                {"id": 2, "name": "ステージ２", "stage_index": 1, "rule": "ステージ２のルールです．"},
            ],
        )

    def test_get_one_stage(self):
        """ID=1のステージを取得"""
        # GET
        response = self.client.get("/stageapi/stages/1/", format="json")
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
                "stage_index": 10,
                "rule": "This is rules of stage1.",
            },
        )
