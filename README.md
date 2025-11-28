# vrchat-invite-notifier

VRChatで届いたインバイトやリクエストインバイトをDiscordにリアルタイム通知するツール

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 概要

VRChatを起動していなくてもインバイトやリクエストインバイトをDiscordで受け取れるツールです。

**✨ 特徴**
- VRChatを起動していなくても通知を受け取れる
- インバイトとリクエストインバイト両方に対応
- メッセージ内容もDiscordに表示
- 2段階認証(TOTP)対応
- 自動再接続機能搭載

## 使い方

### 1. Discord Webhook URLの取得

1. Discordサーバーで通知を受け取りたいチャンネルを選択
2. チャンネル設定 → 連携サービス → Webhook → 新しいWebhook
3. Webhook URLをコピー

### 2. プログラムのダウンロード

[GitHubのReleases](https://github.com/index-0427/vrchat-invite-notifier/releases)から最新の`.exe`ファイルをダウンロードしてください。

### 3. 起動と設定

1. ダウンロードした`vrchat-invite-notifier.exe`を実行
2. GUI画面が表示されるので以下の情報を入力：
   - **VRChat ユーザー名**: VRChatのログインユーザー名
   - **VRChat パスワード**: VRChatのパスワード
   - **Discord Webhook URL**: 上記で取得したWebhook URL
3. 「設定を保存する」にチェックを入れると、次回起動時に自動で読み込まれます(パスワード除く)
4. 「開始」ボタンをクリック
5. 2段階認証が有効な場合、認証コード入力を求められます
6. ログイン成功後、インバイト通知の監視が開始されます
7. VRChatでインバイトやインバイトリクエストを受信すると、自動的にDiscordに通知されます
8. 停止する場合は「停止」ボタンをクリック

## トラブルシューティング

### ログインに失敗する
- ユーザー名とパスワードが正しいか確認してください
- 2段階認証が有効な場合、認証コードを正しく入力してください

### Discord通知が届かない
- Webhook URLが正しいか確認してください
- Webhookが削除されていないか確認してください

## ライセンス

MIT License
