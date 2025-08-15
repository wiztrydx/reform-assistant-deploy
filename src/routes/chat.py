from flask import Blueprint, request, jsonify
import requests
import os
import json

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Claude APIキーを環境変数から取得
        api_key = os.getenv('CLAUDE_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured'}), 500
        
        # Claude APIへのリクエスト
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        }
        
        # リクエストデータの構築
        claude_request = {
            'model': 'claude-3-sonnet-20240229',
            'max_tokens': 1000,
            'messages': data.get('messages', [])
        }
        
        # Claude APIを呼び出し
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=claude_request,
            timeout=30
        )
        
        if response.status_code == 200:
            claude_response = response.json()
            return jsonify({
                'success': True,
                'response': claude_response.get('content', [{}])[0].get('text', '')
            })
        else:
            return jsonify({
                'error': f'Claude API error: {response.status_code}',
                'details': response.text
            }), 500
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@chat_bp.route('/initial-message', methods=['POST'])
def initial_message():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Claude APIキーを環境変数から取得
        api_key = os.getenv('CLAUDE_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured'}), 500
        
        # フォームデータから初回メッセージのプロンプトを生成
        form_data = data.get('formData', {})
        
        prompt = f"""あなたはリフォーム熊本の専門アドバイザーです。お客様情報を元に、4つの異なるリフォームプランを提案してください。

お客様情報:
- 家族構成: {', '.join([f"{m.get('relationship', '')}({m.get('age', '')}歳・{m.get('gender', '')})" for m in form_data.get('familyMembers', [])])}
- ペット: {'なし' if form_data.get('pets', {}).get('none') else f"{form_data.get('pets', {}).get('dogs', {}).get('count', '') + '頭の犬 ' if form_data.get('pets', {}).get('dogs', {}).get('checked') else ''}{form_data.get('pets', {}).get('cats', {}).get('count', '') + '頭の猫 ' if form_data.get('pets', {}).get('cats', {}).get('checked') else ''}{form_data.get('pets', {}).get('other', {}).get('type', '') if form_data.get('pets', {}).get('other', {}).get('checked') else ''}"}
- リフォーム箇所: {', '.join(form_data.get('reformAreas', []))}
- お悩み: {', '.join(form_data.get('reformReasons', []))}
- こだわり: {', '.join(form_data.get('otherPreferences', []))}
- インテリア: {', '.join(form_data.get('interiorStyle', []))}
- 趣味: {', '.join(form_data.get('hobbies', []))}
- ライフスタイル: {', '.join(form_data.get('lifestyle', []))}

以下の形式で4つのプランを提案してください（マークダウンは使わない）：
1. プラン名（絵文字付き）
   概要説明（2-3行）
   
2. プラン名（絵文字付き）
   概要説明（2-3行）
   
3. プラン名（絵文字付き）
   概要説明（2-3行）
   
4. プラン名（絵文字付き）
   概要説明（2-3行）

最後に「どのプランがお気に入りですか？番号で教えてください！」と聞いてください。"""
        
        # Claude APIへのリクエスト
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        }
        
        claude_request = {
            'model': 'claude-3-sonnet-20240229',
            'max_tokens': 1000,
            'messages': [
                {'role': 'user', 'content': prompt}
            ]
        }
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=claude_request,
            timeout=30
        )
        
        if response.status_code == 200:
            claude_response = response.json()
            return jsonify({
                'success': True,
                'response': claude_response.get('content', [{}])[0].get('text', '')
            })
        else:
            # フォールバック応答を生成
            fallback_response = generate_fallback_response(form_data)
            return jsonify({
                'success': True,
                'response': fallback_response,
                'fallback': True
            })
            
    except Exception as e:
        # エラー時もフォールバック応答を返す
        form_data = data.get('formData', {}) if data else {}
        fallback_response = generate_fallback_response(form_data)
        return jsonify({
            'success': True,
            'response': fallback_response,
            'fallback': True
        })

def generate_fallback_response(form_data):
    """フォールバック応答を生成"""
    plans = []
    reform_areas = form_data.get('reformAreas', [])
    reform_reasons = form_data.get('reformReasons', [])
    
    if 'キッチン' in reform_areas:
        plans.append('🍳 家族団らんキッチンプラン\n対面式キッチンで家族との会話を楽しみながら料理ができる空間に。最新のIH調理器と大容量の収納で使い勝手も抜群です！')
    
    if 'お風呂' in reform_areas:
        plans.append('🛁 癒しのスパ風呂プラン\nヒートショック対策の暖房機能付きで安心。大きな窓から光が差し込む、まるで温泉旅館のような癒し空間を実現します！')
    
    if '狭い' in reform_reasons:
        plans.append('📐 空間マジック収納プラン\nデッドスペースを活用した壁面収納や、可動式の間仕切りで限られた空間を最大限活用。見た目もスッキリ、暮らしも快適に！')
    
    if '暗い' in reform_reasons:
        plans.append('☀️ 光あふれる明るい家プラン\n大きな窓の設置や、天窓の追加で自然光をたっぷり取り込む設計。LED照明との組み合わせで24時間明るく快適な空間に！')
    
    # 最低4つのプランを確保
    while len(plans) < 4:
        if not any('エコ' in p for p in plans):
            plans.append('🌱 エコ＆省エネプラン\n断熱性能を高めて光熱費を削減。太陽光パネルや蓄電池の設置で、環境にもお財布にも優しい住まいを実現！')
        elif not any('バリアフリー' in p for p in plans):
            plans.append('♿ 安心バリアフリープラン\n段差をなくし、手すりを設置して家族みんなが安心して暮らせる住まいに。将来を見据えた優しい設計です！')
        else:
            plans.append('🏡 トータルリノベーションプラン\n間取りから設備まで全面的に見直し、まるで新築のような住まいに生まれ変わります。あなただけの理想の空間を実現！')
    
    return f"""こんにちは！リフォーム熊本のAIアドバイザーです！🏠✨

お客様のご要望を拝見させていただきました。
{', '.join(reform_areas)}のリフォームをご検討なんですね！

お客様にピッタリの4つのプランをご提案させていただきます！

{chr(10).join([f"{i+1}. {plan}" for i, plan in enumerate(plans)])}

どのプランがお気に入りですか？番号で教えてください！😊
もちろん、複数のプランを組み合わせることも可能ですよ！"""

