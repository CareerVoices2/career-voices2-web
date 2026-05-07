from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)


@app.route('/page1')
def page1():
    return render_template('index.html')


@app.route('/page2')
def page2():
    return render_template('voice.html')


if __name__ == '__main__':
    print("フロント確認用サーバー：")
    app.run(debug=True)
