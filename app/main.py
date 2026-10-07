from dotenv import load_dotenv
from flask import Flask, render_template
import html
import os
import random

from api.voices import Voices

load_dotenv()

app = Flask(__name__, static_folder='static')


def _markdown_to_html(markdown_text):
    if not markdown_text:
        return ''

    blocks = [
        block.strip()
        for block in str(markdown_text).split('\n\n')
        if block.strip()
    ]
    html_blocks = []

    for block in blocks:
        if block.startswith('### '):
            html_blocks.append(f"<h3>{html.escape(block[4:].strip())}</h3>")
        elif block.startswith('## '):
            html_blocks.append(f"<h2>{html.escape(block[3:].strip())}</h2>")
        elif block.startswith('# '):
            html_blocks.append(f"<h1>{html.escape(block[2:].strip())}</h1>")
        else:
            escaped_block = html.escape(block).replace('\n', '<br>')
            html_blocks.append(f"<p>{escaped_block}</p>")

    return ''.join(html_blocks)


def _get_voices_client():
    return Voices(os.getenv('VOICE_API_URL'), os.getenv('API_TOKEN'))


# トップページ
@app.route('/')
def index():
    voices = []

    try:
        voices = _get_voices_client().get_voices() or []
    except Exception:
        voices = []

    return render_template('index.html', voices=voices)


@app.route('/voice/<string:id>')
def voice_detail(id):
    voices = []
    voice = {}

    try:
        voices_client = _get_voices_client()
        voices = voices_client.get_voices() or []
        voice = voices_client.get_voice_detail(id) or {}
    except Exception:
        voices = []
        voice = {}

    voice = dict(voice) if isinstance(voice, dict) else {}
    voice['voice'] = _markdown_to_html(voice.get('voice', ''))

    other_voice_candidates = [
        current_voice for current_voice in voices
        if isinstance(current_voice, dict) and current_voice.get('id') != id
    ]

    sample_size = min(5, len(other_voice_candidates))
    if sample_size > 0:
        other_voices = random.sample(other_voice_candidates, sample_size)
    else:
        other_voices = []

    return render_template(
        'voice.html',
        voice=voice,
        other_voices=other_voices
    )


if __name__ == '__main__':
    app.run(debug=True)
