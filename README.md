# vrchat-invite-notifier

VRChatで届いたインバイトやリクエストインバイトをDiscordにリアルタイム通知するツール

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)]()

## 概要

VRChat WebSocket API（通称 "the pipeline"）を使用してインバイト通知を監視し、Discord Webhookでチャンネルに通知を送信します。

**✨ 特徴**
- VRChatを起動していなくても通知を受け取れる
- インバイトとリクエストインバイト両方に対応
- メッセージ内容もDiscordに表示
- 2段階認証（TOTP）対応
- 自動再接続機能搭載

## アーキテクチャ

```
VRChat WebSocket API (wss://pipeline.vrchat.cloud)
    ↓ (Notification Event)
[vrchat-invite-notifier]
    ↓ (HTTP POST)
Discord Webhook
    ↓
Discordチャンネル
```

### 動作フロー

1. VRChat APIで認証（ユーザー名/パスワード or 認証クッキー）
2. WebSocketに接続（`notification`イベントをリッスン）
3. インバイト関連の通知を受信
   - `invite`: 通常のインバイト
   - `requestInvite`: インバイトリクエスト
4. 通知内容をパースしてDiscord Webhookに送信

## 技術スタック

### 言語・ランタイム
- **Python 3.10+**

### 主要ライブラリ
- `websockets` - WebSocket通信
- `requests` - HTTP Client (VRChat API認証・Discord Webhook送信用)
- `python-dotenv` - 環境変数管理

### 実行ファイル化
- `PyInstaller` - .exe化

### 設定管理
- 環境変数 (`.env`) または 設定ファイル（`config.json`）

## プロジェクト構造

```
vrchat-invite-notifier/
├── src/
│   ├── __init__.py
│   ├── main.py              # エントリーポイント
│   ├── vrchat/
│   │   ├── __init__.py
│   │   ├── auth.py          # VRChat認証
│   │   └── websocket.py     # WebSocket接続
│   ├── discord/
│   │   ├── __init__.py
│   │   └── webhook.py       # Discord Webhook送信
│   ├── config/
│   │   ├── __init__.py
│   │   └── loader.py        # 設定ファイル読み込み
│   └── utils/
│       └── __init__.py
├── config.example.json      # 設定サンプル
├── .env.example             # 環境変数サンプル
├── requirements.txt         # Python依存関係
├── run.py                   # 開発用実行スクリプト
├── run.bat                  # Windows実行バッチ
├── run.sh                   # Linux/Mac実行シェル
├── build.py                 # .exe化ビルドスクリプト
├── .gitignore
├── README.md
└── LICENSE
```

## 機能

### 実装済み
- ✅ VRChat WebSocket APIへの接続
- ✅ インバイト通知の受信
- ✅ リクエストインバイト通知の受信
- ✅ Discord Webhookへの通知送信
- ✅ 認証情報の安全な管理（config.json / 環境変数）
- ✅ 2段階認証（TOTP）対応
- ✅ 自動再接続処理（WebSocket切断時）
- ✅ .exe化対応（PyInstaller）

### 今後の拡張案
- [ ] 通知フィルタリング（特定ユーザーのみ等）
- [ ] 通知テンプレートのカスタマイズ
- [ ] 複数Discord Webhookへの同時送信
- [ ] ログファイル出力
- [ ] GUI版の作成

## 設定ファイル仕様

### config.json (例)
```json
{
  "vrchat": {
    "username": "your_vrchat_username",
    "password": "your_vrchat_password"
  },
  "discord": {
    "webhook_url": "https://discord.com/api/webhooks/..."
  },
  "options": {
    "notify_types": ["invite", "requestInvite"],
    "auto_reconnect": true,
    "log_level": "info"
  }
}
```

### 環境変数
```bash
VRCHAT_USERNAME=your_username
VRCHAT_PASSWORD=your_password
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

## セットアップ手順

### 方法1: Python環境で実行（推奨）

#### 1. リポジトリのクローン
```bash
git clone https://github.com/index-0427/vrchat-invite-notifier.git
cd vrchat-invite-notifier
```

#### 2. 仮想環境の作成（推奨）
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

#### 4. 設定ファイルの作成

**方法A: config.jsonを使用**
```bash
cp config.example.json config.json
```

`config.json`を編集：
```json
{
  "vrchat": {
    "username": "あなたのVRChatユーザー名",
    "password": "あなたのVRChatパスワード"
  },
  "discord": {
    "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
  },
  "options": {
    "notify_types": ["invite", "requestInvite"],
    "auto_reconnect": true,
    "log_level": "info"
  }
}
```

**方法B: 環境変数を使用**
```bash
cp .env.example .env
```

`.env`を編集：
```
VRCHAT_USERNAME=あなたのVRChatユーザー名
VRCHAT_PASSWORD=あなたのVRChatパスワード
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_URL
```

#### 5. Discord Webhook URLの取得

1. Discordサーバーで通知を受け取りたいチャンネルを選択
2. チャンネル設定 → 連携サービス → Webhook → 新しいWebhook
3. Webhook URLをコピーして設定ファイルに貼り付け

#### 6. 実行

```bash
# Windows
python run.py
# または
run.bat

# Linux / Mac
python3 run.py
# または
./run.sh
```

### 方法2: .exeファイルとして実行（Windows）

#### 1. ビルド
```bash
# 仮想環境をアクティベート後
python build.py
```

#### 2. 実行
```bash
cd dist
vrchat-invite-notifier.exe
```

**注意**: .exe実行時は、実行ファイルと同じディレクトリに`config.json`または`.env`を配置してください。

## 使い方

### 本番実行

1. プログラムを起動すると、VRChatへのログインが開始されます
2. 2段階認証が有効な場合、認証コードの入力を求められます
3. ログイン成功後、自動的にWebSocketに接続し、インバイト通知の監視を開始します
4. VRChatでインバイトやインバイトリクエストを受信すると、自動的にDiscordに通知されます
5. プログラムを終了する場合は `Ctrl+C` を押してください

### Discord通知のテスト

VRChatからの実際のインバイトを待たずに、Discord通知機能をテストできます：

```bash
python test_notification.py
```

このスクリプトは以下の2種類のテスト通知をDiscordに送信します：
- インバイト通知のサンプル
- リクエストインバイト通知のサンプル

## トラブルシューティング

### ログインに失敗する
- ユーザー名とパスワードが正しいか確認してください
- 2段階認証が有効な場合、認証コードを正しく入力してください

### Discord通知が届かない
- Webhook URLが正しいか確認してください
- Webhookが削除されていないか確認してください
- Discordサーバーの権限設定を確認してください

### WebSocketが切断される
- インターネット接続を確認してください
- 自動再接続機能が有効な場合、5秒後に自動的に再接続を試みます

## 開発

### 実装済み
- ✅ Python技術スタック確定
- ✅ VRChat API認証実装（2FA対応）
- ✅ WebSocket接続実装
- ✅ 通知パース実装
- ✅ Discord Webhook送信実装
- ✅ エラーハンドリング・再接続処理
- ✅ ドキュメント整備
- ✅ PyInstallerビルド設定

### 今後の開発予定
- [ ] ログファイル出力機能
- [ ] ユニットテスト実装
- [ ] 通知フィルタリング機能
- [ ] GUI版の作成

## 参考資料

- [VRChat API Documentation](https://vrchat.community/)
- [VRChat WebSocket API](https://vrchat.community/websocket)
- [Discord Webhook Guide](https://discord.com/developers/docs/resources/webhook)

## ライセンス

MIT License
