import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import asyncio
import sys
import json
from pathlib import Path
from vrchat.auth import VRChatAuth
from vrchat.websocket import VRChatWebSocket
from discord.webhook import DiscordWebhook


class InviteNotifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VRChat Invite Notifier")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.vrchat_ws = None
        self.is_running = False
        self.config_file = Path("gui_config.json")

        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(main_frame, text="VRChat Invite Notifier", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(main_frame, text="VRChat ユーザー名:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(main_frame, width=40)
        self.username_entry.grid(row=1, column=1, pady=5, padx=(10, 0))

        ttk.Label(main_frame, text="VRChat パスワード:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(main_frame, width=40, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, padx=(10, 0))

        ttk.Label(main_frame, text="Discord Webhook URL:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.webhook_entry = ttk.Entry(main_frame, width=40)
        self.webhook_entry.grid(row=3, column=1, pady=5, padx=(10, 0))

        self.save_config_var = tk.BooleanVar(value=True)
        save_check = ttk.Checkbutton(main_frame, text="設定を保存する", variable=self.save_config_var)
        save_check.grid(row=4, column=0, columnspan=2, pady=10)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.start_button = ttk.Button(button_frame, text="開始", command=self.start_monitoring, width=15)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(button_frame, text="停止", command=self.stop_monitoring, width=15, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(main_frame, text="ログ:", font=("Arial", 10, "bold")).grid(row=7, column=0, columnspan=2, sticky=tk.W)

        self.log_text = scrolledtext.ScrolledText(main_frame, width=60, height=12, state=tk.DISABLED, wrap=tk.WORD)
        self.log_text.grid(row=8, column=0, columnspan=2, pady=(5, 0))

        self.status_label = ttk.Label(main_frame, text="準備完了", foreground="gray")
        self.status_label.grid(row=9, column=0, columnspan=2, pady=(10, 0))

    def log(self, message):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)

    def update_status(self, message, color="gray"):
        self.status_label.configure(text=message, foreground=color)

    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.username_entry.insert(0, config.get("username", ""))
                    self.webhook_entry.insert(0, config.get("webhook_url", ""))
                    self.log("設定を読み込みました")
            except Exception as e:
                self.log(f"設定の読み込みに失敗: {e}")

    def save_config(self):
        if self.save_config_var.get():
            try:
                config = {
                    "username": self.username_entry.get(),
                    "webhook_url": self.webhook_entry.get()
                }
                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                self.log("設定を保存しました")
            except Exception as e:
                self.log(f"設定の保存に失敗: {e}")

    def start_monitoring(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        webhook_url = self.webhook_entry.get().strip()

        if not username or not password or not webhook_url:
            messagebox.showerror("エラー", "すべての項目を入力してください")
            return

        self.save_config()

        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        self.is_running = True

        self.log("=" * 50)
        self.log("監視を開始します...")
        self.update_status("起動中...", "orange")

        thread = threading.Thread(target=self.run_monitoring, args=(username, password, webhook_url), daemon=True)
        thread.start()

    def stop_monitoring(self):
        self.is_running = False
        if self.vrchat_ws:
            self.vrchat_ws.stop()

        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
        self.log("監視を停止しました")
        self.update_status("停止", "red")

    def run_monitoring(self, username, password, webhook_url):
        try:
            self.log("VRChatにログイン中...")

            auth = VRChatAuth(username, password)
            if not auth.login():
                self.log("❌ ログインに失敗しました")
                self.update_status("ログイン失敗", "red")
                self.root.after(0, lambda: self.start_button.configure(state=tk.NORMAL))
                self.root.after(0, lambda: self.stop_button.configure(state=tk.DISABLED))
                return

            auth_token = auth.get_auth_token()
            if not auth_token:
                self.log("❌ 認証トークンの取得に失敗しました")
                self.update_status("認証失敗", "red")
                self.root.after(0, lambda: self.start_button.configure(state=tk.NORMAL))
                self.root.after(0, lambda: self.stop_button.configure(state=tk.DISABLED))
                return

            self.log("✅ ログイン成功")
            self.log("WebSocketに接続中...")

            discord_webhook = DiscordWebhook(webhook_url)

            self.vrchat_ws = VRChatWebSocket(auth_token, ["invite", "requestInvite"], auto_reconnect=True)
            self.vrchat_ws.set_notification_callback(lambda notif: self.on_notification(notif, discord_webhook))

            self.log("✅ WebSocket接続成功")
            self.log("インバイト通知の監視を開始しました")
            self.update_status("監視中", "green")

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.vrchat_ws.connect())

        except Exception as e:
            self.log(f"❌ エラー: {e}")
            self.update_status("エラー", "red")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: self.start_button.configure(state=tk.NORMAL))
            self.root.after(0, lambda: self.stop_button.configure(state=tk.DISABLED))

    def on_notification(self, notification, discord_webhook):
        notification_type = notification.get("type", "")
        sender = notification.get("senderUsername", "Unknown")

        self.log(f"\n📬 {notification_type} 受信")
        self.log(f"送信者: {sender}")

        success = discord_webhook.send_invite_notification(notification)
        if success:
            self.log("✅ Discord通知送信成功")
        else:
            self.log("❌ Discord通知送信失敗")


def main():
    root = tk.Tk()
    app = InviteNotifierGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
