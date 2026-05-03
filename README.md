# CareerVoices2
就活のリアルな声を．．．

## 開発環境
### 起動方法
```bash
# appディレクトリに移動する
cd app
# 開発用サーバーを起動する
python3 main.py
```
### アクセス方法
http://localhost:5000

## 本番環境
### 起動方法
```bash
# ビルド
docker compose build
# 起動
docker compose up -d
# 終了
docker compose down
```
### アクセス方法
http://localhost:80

## テスト
```bash
# テストディレクトリ全体をテスト
python -m unittest discover -s tests -v
# 指定したテストを実行（例：test_index.py）
python -m unittest tests.test_index -v
```

## リンター
```bash
# appディレクトリに移動する
cd app
# appディレクトリ全体に対してリンターを実行
flake8 .
# 特定のファイルに対してリンターを実行（例：main.py）
flake8 main.py
```

## 環境変数ファイル
- 本番環境
    - `app/.env`
- 開発環境
    - `.env`
```
VOICE_API_URL=voice_api_url
```
