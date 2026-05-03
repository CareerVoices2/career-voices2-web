import unittest
from main import app


class TestIndex(unittest.TestCase):
    def setUp(self):
        """
        テストクライアントのセットアップ
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        """
        インデックスページへのアクセス
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
