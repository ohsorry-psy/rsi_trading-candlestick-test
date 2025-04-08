from flask import Flask, render_template, request, send_from_directory, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    symbol = request.form['symbol']
    start = request.form['start']
    end = request.form['end']

    # generate_chart.py 실행
    result = subprocess.run(
        ['python', 'generate_chart.py', symbol, start, end],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )

    print("stdout:", result.stdout)
    print("stderr:", result.stderr)

    # 저장된 이미지 경로 (Flask static 폴더 기준)
    chart_filename = f"{symbol}.png"
    chart_path = os.path.join(app.root_path, 'static', 'charts', chart_filename)

    # 존재 여부 확인 및 반환
    if os.path.exists(chart_path):
        return jsonify({
            'status': 'ok',
            'image_url': f'/static/charts/{chart_filename}'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': '이미지 생성 실패'
        }), 500

@app.route('/static/charts/<path:filename>')
def serve_chart(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'charts'), filename)

if __name__ == '__main__':
    app.run(debug=True)

from flask_cors import CORS
from flask_cors import CORS

# Flask 앱 생성
app = Flask(__name__)
CORS(app)  # CORS 활성화

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=10000)