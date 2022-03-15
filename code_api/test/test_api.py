import json
from django.test import TestCase
from rest_framework.test import APIClient

from world_api.models import World
from stage_api.models import Stage
from step_api.models import Step
from code_api.models import ProgrammingLanguage
from users.models import User


class CodeAPITests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        # クライアント作成(TODO:ログイン必須になった場合，修正が必要)
        self.client = APIClient(enforce_csrf_checks=True)

        # Step, Userの作成
        world = World.objects.create(
            name="World",
            description="This is descriptions of this world.",
            movie_url="http://hoge.com/hogehoge",
            index=10,
        )
        stage = Stage.objects.create(
            index=5,
            objective="This is rules of this stage.",
            movie_url="http://hoge.com/hogehoge",
            world=world,
        )
        self.step1 = Step.objects.create(
            objective="This is objectives of this step1.",
            description="This is descriptions of this step1.",
            index=3,
            stage=stage,
        )
        self.step2 = Step.objects.create(
            objective="This is objectives of this step2.",
            description="This is descriptions of this step2.",
            index=5,
            stage=stage,
        )
        self.lang_python = ProgrammingLanguage.objects.create(name="Python")
        self.lang_javascript = ProgrammingLanguage.objects.create(name="JavaScript")

        # 一人目のユーザ
        self.user1 = User.objects.create(
            id="fawe;ojifa;woef",
            display_name="hello",
            email="feaw@fawe.com",
            picture="http://localhost:8000/users/auth",
            is_staff=True,
        )

        # 二人目のユーザ
        self.user2 = User.objects.create(
            id="fawe;oasdfa;woef",
            display_name="hello_user2",
            email="feawaaaaa@fawe.com",
            picture="http://localhost:8000/users/auth",
        )

        # ユーザ強制ログイン
        self.client.force_authenticate(user=self.user1)

        # データ準備
        data1 = self.client.post(
            "/codes/",
            {
                "code_content": "print('hello world!')",
                "language": self.lang_python.id,
                "step": self.step1.id,
            },
            format="json",
        )
        data2 = self.client.post(
            "/codes/",
            {
                "code_content": "Alert('hello world!')",
                "language": self.lang_javascript.id,
                "step": self.step2.id,
            },
            format="json",
        )

        # ユーザ強制ログイン
        self.client.force_authenticate(user=self.user2)

        data3 = self.client.post(
            "/codes/",
            {
                "code_content": "pass",
                "language": self.lang_python.id,
                "step": self.step2.id,
            },
            format="json",
        )

        # ログアウト
        self.client.logout()

        # idとタイムスタンプの記録
        data1 = json.loads(data1.content.decode("utf-8"))
        data2 = json.loads(data2.content.decode("utf-8"))
        data3 = json.loads(data3.content.decode("utf-8"))

        self.test_id1 = data1["id"]
        self.test_id2 = data2["id"]
        self.test_id3 = data3["id"]

        # 想定データを作成
        self.res_data1 = {
            "id": self.test_id1,
            "codeContent": "print('hello world!')",
            "language": self.lang_python.id,
            "step": self.step1.id,
            "user": self.user1.id,
            "updatedAt": data1["updatedAt"],
            "createdAt": data1["createdAt"],
        }
        self.res_data2 = {
            "id": self.test_id2,
            "codeContent": "Alert('hello world!')",
            "language": self.lang_javascript.id,
            "step": self.step2.id,
            "user": self.user1.id,
            "updatedAt": data2["updatedAt"],
            "createdAt": data2["createdAt"],
        }
        self.res_data3 = {
            "id": self.test_id3,
            "codeContent": "pass",
            "language": self.lang_python.id,
            "step": self.step2.id,
            "user": self.user2.id,
            "updatedAt": data3["updatedAt"],
            "createdAt": data3["createdAt"],
        }

    def test_get_list_of_all_codes(self):
        """全コードのリストを取得"""
        # GET
        response = self.client.get("/codes/", format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                self.res_data1,
                self.res_data2,
                self.res_data3,
            ],
        )

    def test_get_one_code(self):
        """ID=self.test_id1のステージを取得"""
        # GET
        response = self.client.get(f"/codes/{self.test_id1}/", format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(body, self.res_data1)

    def test_get_filtered_codes_with_language(self):
        """language.nameでフィルターして取得"""
        # GET
        response = self.client.get(
            "/codes/", {"language": self.lang_python.name}, format="json"
        )
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                self.res_data1,
                self.res_data3,
            ],
        )

    def test_get_filtered_codes_with_step(self):
        """step.idでフィルターして取得"""
        # GET
        response = self.client.get("/codes/", {"step": self.step2.id}, format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                self.res_data2,
                self.res_data3,
            ],
        )

    def test_get_filtered_codes_with_user(self):
        """user.idでフィルターして取得"""
        # GET
        response = self.client.get("/codes/", {"user": self.user1.id}, format="json")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                self.res_data1,
                self.res_data2,
            ],
        )

    def test_get_ordered_by_created_at(self):
        """created_atでソートして取得"""
        # GET
        response = self.client.get(
            "/codes/", {"order_by": "-created_at"}, format="json"
        )
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                self.res_data3,
                self.res_data2,
                self.res_data1,
            ],
        )

    def test_get_ordered_by_updated_at(self):
        """updated_atでソートして取得"""
        # データを更新するためログイン
        self.client.force_authenticate(user=self.user1)
        # 一件だけ更新
        updated = self.client.patch(
            f"/codes/{self.test_id1}/",
            {"codeContent": "print('update!')"},
            format="json",
        )
        # レスポンスのステータスコードをチェック
        self.assertEquals(updated.status_code, 200)
        # ログアウト
        self.client.logout()
        # 想定テストデータの更新
        updated_data = json.loads(updated.content.decode("utf-8"))
        self.res_data1 = {
            **self.res_data1,
            "codeContent": "print('update!')",
            "updatedAt": updated_data["updatedAt"],
        }

        # GET
        response = self.client.get(
            "/codes/", {"order_by": "-updated_at"}, format="json"
        )
        # レスポンスのステータスコードをチェック
        self.assertEquals(response.status_code, 200)
        # jsonをデコード
        body = json.loads(response.content.decode("utf-8"))
        # データチェック
        self.assertEquals(
            body,
            [
                {**self.res_data1, "codeContent": "print('update!')"},  # 更新したデータが先頭に来る
                self.res_data3,
                self.res_data2,
            ],
        )

    def test_update_invalid_user(self):
        """作成者以外が編集しようとした時にアクセスを拒否する"""
        # ユーザ1としてログイン
        self.client.force_authenticate(user=self.user1)
        # データ1の編集
        data1_edit = self.client.patch(
            f"/codes/{self.test_id1}/",
            {"codeContent": "print('update!')"},
            format="json",
        )
        # データ3の閲覧
        data3_view = self.client.get(f"/codes/{self.test_id3}/", format="json")
        # データ3の編集
        data3_edit = self.client.patch(
            f"/codes/{self.test_id3}/",
            {"codeContent": "print('update!')"},
            format="json",
        )
        # データ3の削除
        data3_delete = self.client.delete(f"/codes/{self.test_id3}/", format="json")

        # ログアウト
        self.client.logout()

        # ユーザなしでのデータ3の編集
        data3_edit_Annonimous = self.client.post(
            f"/codes/{self.test_id3}/",
            {"codeContent": "print('update!')"},
            format="json",
        )

        # データチェック
        self.assertEquals(data1_edit.status_code, 200)  # 所有者なので編集OK
        self.assertEquals(data3_view.status_code, 200)  # 所有者ではないが閲覧だけなのでOK
        self.assertEquals(data3_edit.status_code, 403)  # 所有者じゃないので編集できない
        self.assertEquals(data3_delete.status_code, 403)  # 所有者じゃないので削除できない
        self.assertEquals(data3_edit_Annonimous.status_code, 401)  # ログインユーザーでなく不正な操作である

    def test_run_code(self):
        """code/:id/runを実行し，実行結果を確認する．"""
        # テストデータが足りないのでデータを追加
        # ユーザ強制ログイン
        self.client.force_authenticate(user=self.user1)

        # データ準備
        self.client.post(
            "/codes/",
            {
                "code_content": "print('for run codes')",
                "language": self.lang_python.id,
                "step": self.step2.id,
            },
            format="json",
        )
        self.client.post(
            "/codes/",
            {
                "code_content": "Alert('for run codes')",
                "language": self.lang_javascript.id,
                "step": self.step1.id,
            },
            format="json",
        )
        # ログアウト
        self.client.logout()

        # code/:id/runを実行
        response1 = self.client.get(
            f"/codes/{self.test_id1}/run/", {"p1": self.test_id2}
        )
        # レスポンスのステータスコードをチェック
        self.assertEquals(response1.status_code, 200)
        # jsonをデコード
        body1 = json.loads(response1.content.decode("utf-8"))
        # ID取得
        result_id = body1["jsonId"]
        # resultAPIからjsonを取得
        response2 = self.client.get(f"/results/{result_id}/")
        # レスポンスのステータスコードをチェック
        self.assertEquals(response2.status_code, 200)
        # jsonをデコード
        body2 = json.loads(response2.content.decode("utf-8"))
        # 指定したコードが入っているか確認
        self.assertEquals(self.test_id1 in body2["codes"], True)
        self.assertEquals(self.test_id2 in body2["codes"], True)
