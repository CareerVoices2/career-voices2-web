import unittest
from api.voices import Voices
from dotenv import load_dotenv
import os

load_dotenv()


class TestVoices(unittest.TestCase):
    def setUp(self):
        """
        Voicesクラスのインスタンスを作成するセットアップ
        """
        self.voices_api_url = os.getenv('VOICES_API_URL_TEST')
        self.voices = Voices(self.voices_api_url)

    def test_get_voices(self):
        """
        get_voicesメソッドのテスト
        """
        voices = self.voices.get_voices()
        self.assertEqual(voices, [
                {
                    "id": "001",
                    "title": "「テスト記事１」",
                    "description": "テスト詳細説明１"
                },
                {
                    "id": "002",
                    "title": "「テスト記事２」",
                    "description": "テスト詳細説明２"
                }
            ]
        )

    def test_get_voice_detail(self):
        """
        get_voice_detailメソッドのテスト
        """
        voice_detail = self.voices.get_voice_detail("001")
        self.assertEqual(voice_detail, {
                "profile":
                {
                    "faculty": "テスト学部",
                    "department": "テスト学科",
                    "graduation_year": 1234,
                    "company": "テスト株式会社",
                    "industry": "テスト業界",
                    "offer_timing": {
                        "grade": 12,
                        "month": 3
                    },
                    "offer_count": 4
                },
                "title": "「テスト記事１」",
                "voice": "テスト記事本文１"
            }
        )
