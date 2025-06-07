#!/usr/bin/env python3
"""
簡易テストサーバー
WebUI接続問題の診断用
"""

from flask import Flask, render_template_string

app = Flask(__name__)

# 最小限のHTMLテンプレート
SIMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MIRRALISM V2 テストサーバー</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        .container { max-width: 600px; margin: 0 auto; text-align: center; }
        h1 { color: #2563eb; }
        .status { background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 MIRRALISM V2</h1>
        <div class="status">
            <h2>✅ サーバー接続成功！</h2>
            <p>WebUIサーバーが正常に動作しています</p>
        </div>
        <p>次のステップ: フル機能のWebUIを起動します</p>
    </div>
</body>
</html>
"""

@app.route('/')
def test_home():
    return render_template_string(SIMPLE_HTML)

@app.route('/test')
def test_endpoint():
    return {"status": "success", "message": "API endpoint working"}

if __name__ == '__main__':
    print("=" * 50)
    print("MIRRALISM V2 テストサーバー")
    print("=" * 50)
    print("ブラウザで以下を開いてください:")
    print("http://localhost:8888")
    print("=" * 50)
    
    app.run(host='127.0.0.1', port=8888, debug=False)