import requests
from typing import Dict, Any
from datetime import datetime


class DiscordWebhook:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_invite_notification(self, notification: Dict[str, Any]) -> bool:
        notification_type = notification.get("type", "")

        if notification_type == "invite":
            return self._send_invite(notification)
        elif notification_type == "requestInvite":
            return self._send_request_invite(notification)
        else:
            print(f"未対応の通知タイプ: {notification_type}")
            return False

    def _send_invite(self, notification: Dict[str, Any]) -> bool:
        sender_username = notification.get("senderUsername", "Unknown")
        details = notification.get("details", {})
        message = details.get("inviteMessage", "")
        world_name = details.get("worldName", "Unknown World")
        created_at = notification.get("created_at", datetime.utcnow().isoformat())

        embed = {
            "title": "📬 VRChat Invite",
            "description": f"**{sender_username}** からインバイトが届きました",
            "fields": [
                {
                    "name": "ワールド",
                    "value": world_name,
                    "inline": False
                }
            ],
            "color": 5814783,
            "timestamp": created_at
        }

        if message:
            embed["fields"].append({
                "name": "メッセージ",
                "value": message,
                "inline": False
            })

        payload = {"embeds": [embed]}
        return self._send_webhook(payload)

    def _send_request_invite(self, notification: Dict[str, Any]) -> bool:
        sender_username = notification.get("senderUsername", "Unknown")
        details = notification.get("details", {})
        message = details.get("requestMessage", "")
        created_at = notification.get("created_at", datetime.utcnow().isoformat())

        embed = {
            "title": "🔔 VRChat Invite Request",
            "description": f"**{sender_username}** からインバイトリクエストが届きました",
            "fields": [],
            "color": 15844367,
            "timestamp": created_at
        }

        if message:
            embed["fields"].append({
                "name": "メッセージ",
                "value": message,
                "inline": False
            })

        payload = {"embeds": [embed]}
        return self._send_webhook(payload)

    def _send_webhook(self, payload: Dict[str, Any]) -> bool:
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            print("✅ Discord通知送信成功")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Discord通知送信エラー: {e}")
            return False
