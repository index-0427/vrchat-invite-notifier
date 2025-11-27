import sys
from pathlib import Path

project_root = Path(__file__).parent
src_dir = project_root / "src"
sys.path.insert(0, str(src_dir))

from discord.webhook import DiscordWebhook
from config.loader import Config
from datetime import datetime


def test_invite_notification():
    print("=" * 50)
    print("Discord通知テスト - インバイト")
    print("=" * 50)
    print()

    config = Config()
    if not config.discord_webhook_url:
        print("エラー: Discord Webhook URLが設定されていません")
        return

    webhook = DiscordWebhook(config.discord_webhook_url)

    test_notification = {
        "type": "invite",
        "senderUsername": "TestUser",
        "message": "テストメッセージ：一緒に遊びませんか？",
        "details": {
            "worldName": "Test World - VRChat Home",
            "worldId": "wrld_test_12345"
        },
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    print("テスト通知を送信中...")
    success = webhook.send_invite_notification(test_notification)

    if success:
        print("\n✅ テスト成功！Discordチャンネルを確認してください。")
    else:
        print("\n❌ テスト失敗。Webhook URLを確認してください。")


def test_request_invite_notification():
    print()
    print("=" * 50)
    print("Discord通知テスト - インバイトリクエスト")
    print("=" * 50)
    print()

    config = Config()
    if not config.discord_webhook_url:
        print("エラー: Discord Webhook URLが設定されていません")
        return

    webhook = DiscordWebhook(config.discord_webhook_url)

    test_notification = {
        "type": "requestInvite",
        "senderUsername": "TestUser2",
        "message": "今どこにいますか？",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    print("テスト通知を送信中...")
    success = webhook.send_invite_notification(test_notification)

    if success:
        print("\n✅ テスト成功！Discordチャンネルを確認してください。")
    else:
        print("\n❌ テスト失敗。Webhook URLを確認してください。")


if __name__ == "__main__":
    print("\nDiscord Webhook通知テスト")
    print("このスクリプトはテスト通知をDiscordに送信します。\n")

    test_invite_notification()
    test_request_invite_notification()

    print()
    print("=" * 50)
    print("テスト完了")
    print("=" * 50)
