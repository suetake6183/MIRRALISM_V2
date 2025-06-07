#!/usr/bin/env python3
"""
MIRRALISM V2 簡易Web UI
=======================

普通の人でも使える、シンプルなWebインターフェース

使い方:
1. python3 simple_web_ui.py
2. ブラウザで http://localhost:8000 を開く
3. URLを貼り付けるか、ファイルをアップロード
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify
from werkzeug.utils import secure_filename

# MIRRALISMシステムのインポート
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from Interface.WebClip import WebClipIntegratedSystem, ResearchMarkdownProcessor

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# システム初期化
webclip_system = WebClipIntegratedSystem()
research_processor = ResearchMarkdownProcessor()

# HTMLテンプレート（1ファイルで完結）
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MIRRALISM V2 - 簡単インターフェース</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            color: #2563eb;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #6b7280;
            font-size: 1.1em;
        }
        
        .main-card {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .tab-container {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            border-bottom: 2px solid #e5e7eb;
        }
        
        .tab {
            padding: 12px 24px;
            background: none;
            border: none;
            font-size: 1.1em;
            cursor: pointer;
            color: #6b7280;
            transition: all 0.3s;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
        }
        
        .tab.active {
            color: #2563eb;
            border-bottom-color: #2563eb;
        }
        
        .tab:hover {
            color: #2563eb;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #374151;
        }
        
        .input-group input[type="url"],
        .input-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        .input-group input[type="url"]:focus,
        .input-group textarea:focus {
            outline: none;
            border-color: #2563eb;
        }
        
        .input-group textarea {
            min-height: 120px;
            resize: vertical;
        }
        
        .file-upload {
            border: 2px dashed #cbd5e1;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #f9fafb;
        }
        
        .file-upload:hover {
            border-color: #2563eb;
            background: #eff6ff;
        }
        
        .file-upload.dragover {
            border-color: #2563eb;
            background: #dbeafe;
        }
        
        .file-upload input {
            display: none;
        }
        
        .file-upload-icon {
            font-size: 3em;
            color: #9ca3af;
            margin-bottom: 10px;
        }
        
        .button {
            background: #2563eb;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
        }
        
        .button:hover {
            background: #1d4ed8;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
        
        .button:disabled {
            background: #9ca3af;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 40px;
        }
        
        .loading.active {
            display: block;
        }
        
        .spinner {
            display: inline-block;
            width: 50px;
            height: 50px;
            border: 4px solid #e5e7eb;
            border-top-color: #2563eb;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .result {
            display: none;
            margin-top: 30px;
        }
        
        .result.active {
            display: block;
        }
        
        .result-card {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
        }
        
        .result-card h3 {
            color: #1f2937;
            margin-bottom: 12px;
            font-size: 1.2em;
        }
        
        .result-card p {
            color: #4b5563;
            margin-bottom: 8px;
        }
        
        .insight {
            background: #eff6ff;
            border: 1px solid #dbeafe;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        .question {
            background: #f0fdf4;
            border: 1px solid #d1fae5;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        .suggestion {
            background: #fef3c7;
            border: 1px solid #fde68a;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        .error {
            background: #fee2e2;
            border: 1px solid #fecaca;
            color: #dc2626;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }
        
        .error.active {
            display: block;
        }
        
        .help-text {
            color: #6b7280;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: #9ca3af;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>MIRRALISM V2</h1>
            <p>あなたの知識獲得と思考を理解するシステム</p>
        </div>
        
        <div class="main-card">
            <div class="tab-container">
                <button class="tab active" onclick="switchTab('webclip')">
                    📰 Web記事をクリップ
                </button>
                <button class="tab" onclick="switchTab('research')">
                    📚 リサーチファイルを分析
                </button>
            </div>
            
            <!-- WebClipタブ -->
            <div id="webclip-tab" class="tab-content active">
                <form id="webclip-form">
                    <div class="input-group">
                        <label for="url">記事のURL</label>
                        <input type="url" id="url" placeholder="https://example.com/article" required>
                        <p class="help-text">分析したい記事のURLを貼り付けてください</p>
                    </div>
                    
                    <div class="input-group">
                        <label for="title">記事のタイトル（オプション）</label>
                        <input type="url" id="title" placeholder="興味深い記事のタイトル">
                    </div>
                    
                    <button type="submit" class="button">
                        この記事を分析する
                    </button>
                </form>
            </div>
            
            <!-- リサーチファイルタブ -->
            <div id="research-tab" class="tab-content">
                <form id="research-form">
                    <div class="input-group">
                        <label>マークダウンファイルをアップロード</label>
                        <div class="file-upload" id="file-upload-area">
                            <div class="file-upload-icon">📁</div>
                            <p>ファイルをドラッグ&ドロップ<br>または<br>クリックして選択</p>
                            <input type="file" id="file-input" accept=".md,.markdown" required>
                        </div>
                        <p class="help-text">Gemini、Perplexity、Claudeなどでリサーチした.mdファイル</p>
                    </div>
                    
                    <button type="submit" class="button" disabled id="analyze-button">
                        リサーチファイルを分析する
                    </button>
                </form>
            </div>
            
            <!-- ローディング表示 -->
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 20px; color: #6b7280;">分析中... あなたの興味を理解しています</p>
            </div>
            
            <!-- エラー表示 -->
            <div class="error" id="error"></div>
            
            <!-- 結果表示 -->
            <div class="result" id="result">
                <h2 style="margin-bottom: 20px; color: #1f2937;">分析結果</h2>
                
                <div class="result-card">
                    <h3>💭 洞察</h3>
                    <div class="insight" id="insight"></div>
                </div>
                
                <div class="result-card">
                    <h3>❓ 質問</h3>
                    <div class="question" id="questions"></div>
                </div>
                
                <div class="result-card">
                    <h3>💡 提案</h3>
                    <div class="suggestion" id="suggestions"></div>
                </div>
                
                <div class="result-card" id="source-info" style="display: none;">
                    <h3>📊 リサーチ情報</h3>
                    <p id="research-source"></p>
                    <p id="research-quality"></p>
                </div>
            </div>
        </div>
        
        <footer>
            <p>MIRRALISM V2 - 知識と成長の科学的管理システム</p>
        </footer>
    </div>
    
    <script>
        // タブ切り替え
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            event.target.classList.add('active');
            document.getElementById(tabName + '-tab').classList.add('active');
            
            // 結果をクリア
            document.getElementById('result').classList.remove('active');
            document.getElementById('error').classList.remove('active');
        }
        
        // ファイルアップロード処理
        const fileUploadArea = document.getElementById('file-upload-area');
        const fileInput = document.getElementById('file-input');
        const analyzeButton = document.getElementById('analyze-button');
        
        fileUploadArea.addEventListener('click', () => fileInput.click());
        
        fileUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUploadArea.classList.add('dragover');
        });
        
        fileUploadArea.addEventListener('dragleave', () => {
            fileUploadArea.classList.remove('dragover');
        });
        
        fileUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                updateFileDisplay();
            }
        });
        
        fileInput.addEventListener('change', updateFileDisplay);
        
        function updateFileDisplay() {
            if (fileInput.files.length > 0) {
                const fileName = fileInput.files[0].name;
                fileUploadArea.innerHTML = `
                    <div class="file-upload-icon">✅</div>
                    <p><strong>${fileName}</strong><br>ファイルが選択されました</p>
                `;
                analyzeButton.disabled = false;
            }
        }
        
        // WebClipフォーム送信
        document.getElementById('webclip-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const url = document.getElementById('url').value;
            const title = document.getElementById('title').value;
            
            showLoading();
            hideError();
            hideResult();
            
            try {
                const response = await fetch('/analyze/webclip', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url, title }),
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showWebClipResult(data.result);
                } else {
                    showError(data.error || '分析中にエラーが発生しました');
                }
            } catch (error) {
                showError('サーバーとの通信に失敗しました');
            } finally {
                hideLoading();
            }
        });
        
        // リサーチファイルフォーム送信
        document.getElementById('research-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (fileInput.files.length === 0) {
                showError('ファイルを選択してください');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            showLoading();
            hideError();
            hideResult();
            
            try {
                const response = await fetch('/analyze/research', {
                    method: 'POST',
                    body: formData,
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showResearchResult(data.result);
                } else {
                    showError(data.error || '分析中にエラーが発生しました');
                }
            } catch (error) {
                showError('サーバーとの通信に失敗しました');
            } finally {
                hideLoading();
            }
        });
        
        // 結果表示関数
        function showWebClipResult(result) {
            const display = result.instant_display;
            
            document.getElementById('insight').innerHTML = `<p>${display.primary_message}</p>`;
            document.getElementById('questions').innerHTML = `<p>${display.question}</p>`;
            document.getElementById('suggestions').innerHTML = `<p>${display.suggestion}</p>`;
            
            document.getElementById('source-info').style.display = 'none';
            document.getElementById('result').classList.add('active');
        }
        
        function showResearchResult(result) {
            const analysis = result.research_analysis;
            const motivation = analysis.motivation_analysis.analysis;
            const insights = analysis.research_insights;
            
            document.getElementById('insight').innerHTML = `<p>${motivation.dialogue.interest_insight}</p>`;
            
            const questions = insights.research_questions.map(q => `<p>• ${q}</p>`).join('');
            document.getElementById('questions').innerHTML = questions;
            
            const suggestions = insights.utilization_suggestions
                .map(s => `<p>• ${s.suggestion}</p>`)
                .join('');
            document.getElementById('suggestions').innerHTML = suggestions;
            
            // リサーチ情報表示
            const source = analysis.source_detection;
            const quality = insights.quality_assessment;
            
            document.getElementById('research-source').innerHTML = 
                `検出ソース: <strong>${source.detected_source.toUpperCase()}</strong> (信頼度: ${Math.round(source.confidence * 100)}%)`;
            document.getElementById('research-quality').innerHTML = 
                `品質評価: <strong>${quality.quality_label}</strong>`;
            
            document.getElementById('source-info').style.display = 'block';
            document.getElementById('result').classList.add('active');
        }
        
        // ユーティリティ関数
        function showLoading() {
            document.getElementById('loading').classList.add('active');
        }
        
        function hideLoading() {
            document.getElementById('loading').classList.remove('active');
        }
        
        function showError(message) {
            const errorEl = document.getElementById('error');
            errorEl.textContent = message;
            errorEl.classList.add('active');
        }
        
        function hideError() {
            document.getElementById('error').classList.remove('active');
        }
        
        function hideResult() {
            document.getElementById('result').classList.remove('active');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """メインページ"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze/webclip', methods=['POST'])
def analyze_webclip():
    """WebClip分析API"""
    try:
        data = request.json
        url = data.get('url')
        title = data.get('title', '')
        
        # 簡易的な記事内容取得（実際はWebスクレイピングが必要）
        # ここではデモ用に固定テキストを使用
        content = f"This is a demo content for {url}. In production, this would fetch actual article content."
        
        # 非同期処理を同期的に実行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(
            webclip_system.process_webclip_complete(
                article_url=url,
                article_title=title or f"Article from {url}",
                article_content=content,
                user_context={"user_type": "general_user"}
            )
        )
        
        return jsonify({
            'success': result['success'],
            'result': result if result['success'] else None,
            'error': result.get('error')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/analyze/research', methods=['POST'])
def analyze_research():
    """リサーチファイル分析API"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'ファイルがありません'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'ファイルが選択されていません'})
        
        # 一時ファイルとして保存
        filename = secure_filename(file.filename)
        temp_path = Path(f"/tmp/{filename}")
        file.save(str(temp_path))
        
        # リサーチファイル分析
        result = research_processor.process_research_markdown(
            markdown_file_path=str(temp_path),
            user_context={"user_type": "general_user"},
            save_to_file=False
        )
        
        # 一時ファイル削除
        temp_path.unlink()
        
        return jsonify({
            'success': result['success'],
            'result': result if result['success'] else None,
            'error': result.get('error')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("=" * 60)
    print("MIRRALISM V2 簡易Web UI")
    print("=" * 60)
    print("\n1. ブラウザで以下のURLを開いてください:")
    print("   http://localhost:8080")
    print("\n2. Web記事のURLを貼り付けるか、")
    print("   リサーチファイルをドラッグ&ドロップしてください")
    print("\n3. 終了するには Ctrl+C を押してください")
    print("=" * 60)
    
    app.run(host='127.0.0.1', port=8080, debug=False)