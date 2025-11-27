import asyncio
import signal
import sys
from config.loader import Config
from vrchat.auth import VRChatAuth
from vrchat.websocket import VRChatWebSocket
from discord.webhook import DiscordWebhook


class InviteNotifier:
    def __init__(self):
        self.config = Config()
        self.vrchat_auth: VRChatAuth = None
        self.vrchat_ws: VRChatWebSocket = None
        self.discord_webhook: DiscordWebhook = None
        self.running = True

    def setup_signal_handlers(self):
        def signal_handler(sig, frame):
            print("\n\n終了シグナルを受信しました。プログラムを終了します...")
            self.running = False
            if self.vrchat_ws:
                self.vrchat_ws.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def initialize(self) -> bool:
        print("=" * 50)
        print("vrchat-invite-notifier")
        print("=" * 50)
        print()

        if not self.config.validate():
            print("\n設定が不正です。config.jsonまたは環境変数を確認してください。")
            return False

        self.discord_webhook = DiscordWebhook(self.config.discord_webhook_url)

        print("VRChatにログイン中...")
        self.vrchat_auth = VRChatAuth(
            self.config.vrchat_username,
            self.config.vrchat_password
        )

        if not self.vrchat_auth.login():
            print("\nVRChatログインに失敗しました。")
            return False

        auth_token = self.vrchat_auth.get_auth_token()
        if not auth_token:
            print("\n認証トークンの取得に失敗しました。")
            return False

        self.vrchat_ws = VRChatWebSocket(
            auth_token,
            self.config.notify_types,
            self.config.auto_reconnect
        )

        self.vrchat_ws.set_notification_callback(self.on_notification)

        print()
        print("=" * 50)
        print("初期化完了！インバイト通知の監視を開始します...")
        print("終了するには Ctrl+C を押してください")
        print("=" * 50)
        print()

        return True

    def on_notification(self, notification: dict):
        self.discord_webhook.send_invite_notification(notification)

    async def run(self):
        if not self.initialize():
            return

        try:
            await self.vrchat_ws.connect()
        except KeyboardInterrupt:
            print("\n\nプログラムを終了します...")
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")
        finally:
            if self.vrchat_ws:
                self.vrchat_ws.stop()


def main():
    notifier = InviteNotifier()
    notifier.setup_signal_handlers()

    try:
        asyncio.run(notifier.run())
    except KeyboardInterrupt:
        print("\nプログラムを終了しました")


if __name__ == "__main__":
    main()
