from django.test import TestCase
from users.models import User


class UserModelsTests(TestCase):
    def setUp(self):  # テストケース実行毎に実行される
        User.objects.create(
            id="fawe;ojifa;woef",
            display_name="hello",
            email="feaw@fawe.com",
            picture="http://localhost:8000/users/auth",
        )

    def test_model_get_user(self):
        """正常系テスト"""
        test1 = User.objects.get(id="fawe;ojifa;woef")
        # 色々チェック
        self.assertEquals(test1.display_name, "hello")
        self.assertEquals(test1.email, "feaw@fawe.com")
        self.assertEquals(test1.picture, "http://localhost:8000/users/auth")
        self.assertEquals(test1.is_staff, False)
