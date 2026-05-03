# 公式のPythonランタイムをベースイメージとして使用
FROM python:3.13
# コンテナ内の作業ディレクトリを設定
WORKDIR /app
# pipを最新バージョンにアップグレード
RUN pip install --upgrade pip
# requirements.txtをコンテナにコピー
COPY requirements.txt /app/
# 必要なPythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt
# アプリケーションのコードをコンテナにコピー
COPY . /app/
# アプリケーションを起動（gunicornを使用してFlaskアプリケーションを実行）
CMD ["gunicorn", "--workers","3", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "main:app"]