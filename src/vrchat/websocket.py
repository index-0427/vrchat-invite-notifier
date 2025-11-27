import asyncio
import websockets
import json
from typing import Callable, List, Optional
from websockets.client import WebSocketClientProtocol


class VRChatWebSocket:
    WEBSOCKET_URL = "wss://pipeline.vrchat.cloud"
    USER_AGENT = "vrchat-invite-notifier/1.0"

    def __init__(self, auth_token: str, notify_types: List[str], auto_reconnect: bool = True):
        self.auth_token = auth_token
        self.notify_types = notify_types
        self.auto_reconnect = auto_reconnect
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.is_running = False
        self.notification_callback: Optional[Callable] = None

    def set_notification_callback(self, callback: Callable):
        self.notification_callback = callback

    async def connect(self):
        url = f"{self.WEBSOCKET_URL}/?authToken={self.auth_token}"
        self.is_running = True

        while self.is_running:
            try:
                print("VRChat WebSocketに接続中...")
                async with websockets.connect(
                    url,
                    user_agent_header=self.USER_AGENT
                ) as websocket:
                    self.websocket = websocket
                    print("VRChat WebSocket接続成功")
                    await self._listen()

            except websockets.exceptions.ConnectionClosed as e:
                print(f"WebSocket接続が切断されました: {e}")
                if self.auto_reconnect and self.is_running:
                    print("5秒後に再接続します...")
                    await asyncio.sleep(5)
                else:
                    break

            except Exception as e:
                print(f"WebSocketエラー: {e}")
                if self.auto_reconnect and self.is_running:
                    print("5秒後に再接続します...")
                    await asyncio.sleep(5)
                else:
                    break

        print("WebSocket接続終了")

    async def _listen(self):
        if not self.websocket:
            return

        async for message in self.websocket:
            try:
                if isinstance(message, str):
                    data = json.loads(message)
                else:
                    data = message

                if isinstance(data, dict):
                    await self._handle_message(data)
                else:
                    print(f"デバッグ: 予期しないメッセージ形式: {type(data)}")
            except json.JSONDecodeError as e:
                print(f"JSONデコードエラー: {e}")
            except Exception as e:
                print(f"メッセージ処理エラー: {e}")
                import traceback
                traceback.print_exc()

    async def _handle_message(self, data: dict):
        msg_type = data.get("type")

        if msg_type == "notification":
            content = data.get("content", {})

            if isinstance(content, str):
                try:
                    content = json.loads(content)
                except json.JSONDecodeError as e:
                    print(f"エラー: 通知のJSONパースに失敗しました: {e}")
                    return

            if not isinstance(content, dict):
                return

            notification_type = content.get("type", "")

            if notification_type in self.notify_types:
                print(f"\n📬 {notification_type} 受信")
                print(f"送信者: {content.get('senderUsername', 'Unknown')}")

                if self.notification_callback:
                    await self._call_notification_callback(content)

        elif msg_type in ["friend-location", "friend-online", "friend-offline",
                          "friend-active", "friend-update", "user-location",
                          "user-update", "see-notification"]:
            pass

    async def _call_notification_callback(self, notification: dict):
        if asyncio.iscoroutinefunction(self.notification_callback):
            await self.notification_callback(notification)
        else:
            self.notification_callback(notification)

    def stop(self):
        self.is_running = False
        if self.websocket:
            asyncio.create_task(self.websocket.close())
