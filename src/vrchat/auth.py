import requests
import base64
from typing import Optional, Dict, Any


class VRChatAuth:
    BASE_URL = "https://api.vrchat.cloud/api/1"
    USER_AGENT = "vrchat-invite-notifier/1.0"

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})
        self.auth_token: Optional[str] = None
        self.user_id: Optional[str] = None

    def login(self) -> bool:
        auth_str = f"{self.username}:{self.password}"
        auth_bytes = auth_str.encode("utf-8")
        auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")

        self.session.headers.update({
            "Authorization": f"Basic {auth_b64}"
        })

        try:
            response = self.session.get(
                f"{self.BASE_URL}/auth/user",
                timeout=10
            )

            if response.status_code == 200:
                user_data = response.json()
                self.user_id = user_data.get("id")
                print(f"ログイン成功: {user_data.get('displayName', 'Unknown')}")
                return self._get_auth_token()

            elif response.status_code == 401:
                print("エラー: ユーザー名またはパスワードが間違っています")
                return False

            else:
                error_data = response.json()
                if error_data.get("requiresTwoFactorAuth"):
                    return self._handle_2fa()
                else:
                    print(f"ログインエラー: {response.status_code} - {error_data}")
                    return False

        except requests.exceptions.RequestException as e:
            print(f"ログインリクエストエラー: {e}")
            return False

    def _handle_2fa(self) -> bool:
        print("\n2段階認証が必要です")
        print("認証コードを入力してください:")

        try:
            code = input("> ")

            response = self.session.post(
                f"{self.BASE_URL}/auth/twofactorauth/totp/verify",
                json={"code": code},
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("verified"):
                    print("2段階認証成功")
                    return self._complete_login()
                else:
                    print("エラー: 認証コードが無効です")
                    return False
            else:
                print(f"2段階認証エラー: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"2段階認証リクエストエラー: {e}")
            return False

    def _complete_login(self) -> bool:
        try:
            response = self.session.get(
                f"{self.BASE_URL}/auth/user",
                timeout=10
            )

            if response.status_code == 200:
                user_data = response.json()
                self.user_id = user_data.get("id")
                print(f"ログイン完了: {user_data.get('displayName', 'Unknown')}")
                return self._get_auth_token()
            else:
                print(f"ログイン完了エラー: {response.status_code}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"ログイン完了リクエストエラー: {e}")
            return False

    def _get_auth_token(self) -> bool:
        cookies = self.session.cookies.get_dict()

        self.auth_token = cookies.get("auth")

        if not self.auth_token:
            for key in cookies.keys():
                if key.startswith("auth"):
                    self.auth_token = cookies.get(key)
                    break

        if not self.auth_token:
            print("エラー: 認証トークンの取得に失敗しました")
            return False

        print("認証トークン取得成功")
        return True

    def get_auth_token(self) -> Optional[str]:
        return self.auth_token
