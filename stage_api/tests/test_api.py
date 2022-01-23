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
            {"stageIndex": 10,
             "objective": "This is rules of stage1.",
            "movieUrl":"http://hoge.com/hogehoge",
            },
            format="json",
        )
        self.client.post(
            "/stages/",
            {"stageIndex": 1,
             "objective": "ステージ２のルールです．",
             "movieUrl":"http://world.com/worldworld",
             },
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
                    "stageIndex": 10,
                    "objective": "This is rules of stage1.",
                    "movieUrl":"http://hoge.com/hogehoge",
                },
                {"id": 2,
                 "stageIndex": 1,
                  "objective": "ステージ２のルールです．",
                  "movieUrl":"http://world.com/worldworld",
                }
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
                "stageIndex": 10,
                "objective": "This is rules of stage1.",
                "movieUrl":"http://hoge.com/hogehoge",
            },
        )

    def test_getfiltered_examples_with_a_field(self):
        """フィルターでstage_idをソートして取得"""
        #GET
        response = self.client.get("/stages/", {
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
                    'stageIndex': 1,
                    'objective': 'ステージ２のルールです．',
                    "movieUrl":"http://world.com/worldworld",
                },
                {
                    'id': 1,
                    'stageIndex': 10,
                    'objective': 'This is rules of stage1.',
                    "movieUrl":"http://hoge.com/hogehoge",
                },   
            ]
        )

