# Netlifyでのデプロイガイド

## 🌍 Netlify

Netlifyは静的サイトホスティングに特化したプラットフォームです。

### ⚠️ 重要な注意事項

Netlifyは**静的サイト専用**のため、バックエンドAPIは別途デプロイが必要です。
このガイドでは、フロントエンドのみをNetlifyにデプロイし、バックエンドは他のサービスを使用します。

### 前提条件

- GitHubアカウント
- Netlifyアカウント（無料）
- バックエンドAPI（Railway、Render等で別途デプロイ済み）

### 手順

#### 1. フロントエンド専用プロジェクトの準備

```bash
# フロントエンド専用ディレクトリを作成
mkdir reform-assistant-frontend-only
cd reform-assistant-frontend-only

# 静的ファイルをコピー
cp -r ../src/static/* ./

# package.jsonを作成（ビルド用）
```

`package.json`:
```json
{
  "name": "reform-assistant-frontend",
  "version": "1.0.0",
  "scripts": {
    "build": "echo 'Static files ready'",
    "start": "echo 'Static files ready'"
  }
}
```

#### 2. APIエンドポイントの更新

`index.html` 内のJavaScriptでAPIエンドポイントを更新:

```javascript
// 例: Railwayにデプロイしたバックエンドを使用
const API_BASE_URL = 'https://your-backend-app.railway.app';
```

#### 3. GitHubリポジトリの作成

```bash
git init
git add .
git commit -m "Frontend for Netlify"
git remote add origin https://github.com/yourusername/reform-assistant-frontend.git
git push -u origin main
```

#### 4. Netlifyでのデプロイ

1. [Netlify](https://netlify.com)にログイン
2. 「New site from Git」をクリック
3. GitHubリポジトリを選択
4. デプロイ設定:
   - **Build command**: `npm run build`
   - **Publish directory**: `./`

#### 5. 環境変数の設定（必要に応じて）

「Site settings」→「Environment variables」で設定

#### 6. カスタムドメインの設定

1. 「Domain settings」をクリック
2. 「Add custom domain」でドメインを追加
3. DNS設定を更新

### 推奨構成: フロントエンド（Netlify）+ バックエンド（Railway）

#### バックエンドをRailwayにデプロイ

```bash
# バックエンドのみのプロジェクトを作成
mkdir reform-assistant-backend-only
cd reform-assistant-backend-only

# バックエンドファイルをコピー
cp -r ../src ./
cp ../requirements.txt ./
cp ../Dockerfile ./

# GitHubにプッシュしてRailwayでデプロイ
```

#### フロントエンドでAPIエンドポイントを更新

```javascript
// Railway のバックエンドURLを指定
const API_BASE_URL = 'https://reform-assistant-production.up.railway.app';
```

### 料金

- **Netlify**: 無料プラン（月100GB帯域幅、300分ビルド時間）
- **Railway**: 月5ドルまで無料（バックエンド用）

### 特徴

- **高速CDN**: 世界中で高速配信
- **自動HTTPS**: SSL証明書自動発行
- **フォーム処理**: 静的フォームの処理機能
- **継続的デプロイ**: GitHubプッシュで自動デプロイ

### 代替案: Netlify Functions

バックエンド機能をNetlify Functionsで実装する場合:

`netlify/functions/chat.js`:
```javascript
exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { messages } = JSON.parse(event.body);
    
    // Claude API呼び出し
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-3-sonnet-20240229',
        max_tokens: 1000,
        messages: messages
      })
    });

    const data = await response.json();
    
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ response: data.content[0].text })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal Server Error' })
    };
  }
};
```

### トラブルシューティング

**ビルドが失敗する場合:**
- `package.json` の設定を確認
- ビルドログを確認

**APIが動作しない場合:**
- CORS設定を確認
- バックエンドのURLが正しいか確認

**フォームが動作しない場合:**
- Netlify Formsの設定を確認
- HTMLフォームに `netlify` 属性を追加

