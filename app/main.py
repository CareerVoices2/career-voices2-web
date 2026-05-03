from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

app = Flask(__name__, static_folder='static')


# トップページ
@app.route('/')
def index():
    # TODO: ボイスのリストを取得して渡す
    return render_template('index.html', voices=None)

# TODO: ボイス詳細ページ（/voice/<id:str>）
# NOTE: voice，other_voicesを取得して渡す
# NOTE: voice.htmlを返す


if __name__ == '__main__':
    app.run(debug=True)
