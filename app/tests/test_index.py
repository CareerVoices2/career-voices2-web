import unittest
from main import app
from unittest.mock import patch


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
        mock_voices = [
            {"id": "001", "title": "記事1", "description": "説明1"},
            {"id": "002", "title": "記事2", "description": "説明2"},
        ]
        with patch('main.Voices') as mock_voices_class, patch('main.render_template', return_value='index-page') as mock_render_template:
            mock_voices_class.return_value.get_voices.return_value = mock_voices
            response = self.app.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'index-page')
        mock_render_template.assert_called_once_with('index.html', voices=mock_voices)

    def test_voice_detail(self):
        """
        ボイス詳細ページへのアクセス
        """
        mock_voices = [{"id": f"{index:03d}", "title": f"記事{index}", "description": f"説明{index}"} for index in range(1, 8)]
        mock_voice_detail = {
            "id": "001",
            "title": "記事1",
            "voice": "# 見出し\n\n本文"
        }

        with patch('main.Voices') as mock_voices_class, patch('main.render_template', return_value='voice-page') as mock_render_template, patch('main.random.sample', side_effect=lambda voices, size: voices[:size]):
            mock_voices_class.return_value.get_voices.return_value = mock_voices
            mock_voices_class.return_value.get_voice_detail.return_value = mock_voice_detail
            response = self.app.get('/voice/001')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'voice-page')
        _, kwargs = mock_render_template.call_args
        self.assertEqual(mock_render_template.call_args.args[0], 'voice.html')
        self.assertEqual(kwargs['voice']['voice'], '<h1>見出し</h1><p>本文</p>')
        self.assertEqual(len(kwargs['other_voices']), 5)
        self.assertTrue(all(voice.get('id') != '001' for voice in kwargs['other_voices']))
