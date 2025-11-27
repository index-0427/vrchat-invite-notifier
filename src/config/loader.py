import json
import os
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

        self.vrchat_username: str = ""
        self.vrchat_password: str = ""
        self.discord_webhook_url: str = ""
        self.notify_types: List[str] = ["invite", "requestInvite"]
        self.auto_reconnect: bool = True
        self.log_level: str = "info"

        self._load_config()

    def _load_config(self):
        config_path = Path("config.json")

        if config_path.exists():
            self._load_from_file(config_path)
        else:
            self._load_from_env()

    def _load_from_file(self, config_path: Path):
        with open(config_path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)

        vrchat_config = data.get("vrchat", {})
        self.vrchat_username = vrchat_config.get("username", "")
        self.vrchat_password = vrchat_config.get("password", "")

        discord_config = data.get("discord", {})
        self.discord_webhook_url = discord_config.get("webhook_url", "")

        options = data.get("options", {})
        self.notify_types = options.get("notify_types", ["invite", "requestInvite"])
        self.auto_reconnect = options.get("auto_reconnect", True)
        self.log_level = options.get("log_level", "info")

        self._override_from_env()

    def _load_from_env(self):
        self.vrchat_username = os.getenv("VRCHAT_USERNAME", "")
        self.vrchat_password = os.getenv("VRCHAT_PASSWORD", "")
        self.discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "")

    def _override_from_env(self):
        env_username = os.getenv("VRCHAT_USERNAME")
        if env_username:
            self.vrchat_username = env_username

        env_password = os.getenv("VRCHAT_PASSWORD")
        if env_password:
            self.vrchat_password = env_password

        env_webhook = os.getenv("DISCORD_WEBHOOK_URL")
        if env_webhook:
            self.discord_webhook_url = env_webhook

    def validate(self) -> bool:
        if not self.vrchat_username:
            print("エラー: VRChatのユーザー名が設定されていません")
            return False

        if not self.vrchat_password:
            print("エラー: VRChatのパスワードが設定されていません")
            return False

        if not self.discord_webhook_url:
            print("エラー: Discord Webhook URLが設定されていません")
            return False

        return True
