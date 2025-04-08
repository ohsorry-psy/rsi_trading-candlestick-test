from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_cors import CORS
import os
from generate_chart import generate_chart

app = Flask(__name__)
CORS(app)  # 외부 도메인에서도 접근 가능하도록 허용

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    symbol = request.form['symbol']
    start = request.form['start']
    end = request.form['end']

    print(f"[요청] symbol={symbol}, start={start}, end={end}")

    try:
        chart_path = generate_chart(symbol, start, end)

        if os.path.exists(chart_path):
            return jsonify({
                'status': 'ok',
                'image_url': f'/static/charts/{symbol}.png'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': '이미지 생성 실패'
            }), 500

    except Exception as e:
        print("[Server Error]", e)
        return jsonify({
            'status': 'error',
            'message': '이미지 생성 실패'
        }), 500

@app.route('/static/charts/<path:filename>')
def serve_chart(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'charts'), filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
