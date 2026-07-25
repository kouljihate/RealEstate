import json
import os
from pathlib import Path

import requests

API_BASE = "http://10.0.2.2:8000/api/v1"  # Android emulator -> host


class ApiService:
    def __init__(self):
        self.token = None
        self.token_path = Path("token.json")

    def get_saved_token(self):
        if self.token_path.exists():
            try:
                data = json.loads(self.token_path.read_text())
                return data.get("access_token")
            except Exception:
                return None
        return None

    def save_token(self, token):
        self.token_path.write_text(json.dumps({"access_token": token}))
        self.token = token

    def set_token(self, token):
        self.token = token
        if token is None and self.token_path.exists():
            self.token_path.unlink()

    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _request(self, method, path, json_data=None, files=None):
        url = f"{API_BASE}{path}"
        try:
            if files:
                h = {}
                if self.token:
                    h["Authorization"] = f"Bearer {self.token}"
                resp = requests.request(method, url, files=files, headers=h, timeout=30)
            else:
                resp = requests.request(method, url, json=json_data, headers=self._headers(), timeout=30)
            resp.raise_for_status()
            if resp.status_code == 204:
                return None
            return resp.json()
        except requests.RequestException as e:
            detail = "Network error"
            try:
                detail = e.response.json().get("detail", str(e))
            except Exception:
                detail = str(e)
            raise Exception(detail)

    def login(self, email, password):
        data = self._request("POST", "/auth/login", {"email": email, "password": password})
        self.save_token(data["access_token"])
        return data

    def register(self, email, username, password, full_name, phone=""):
        return self._request(
            "POST", "/auth/register",
            {"email": email, "username": username, "password": password, "full_name": full_name, "phone": phone},
        )

    def get_me(self):
        return self._request("GET", "/auth/me")

    def get_properties(self, page=1, size=20):
        return self._request("GET", f"/properties?page={page}&size={size}")

    def get_property(self, property_id):
        return self._request("GET", f"/properties/{property_id}")

    def create_property(self, data):
        return self._request("POST", "/properties/", data)

    def upload_media(self, file_path, property_id=None):
        files = {"file": open(file_path, "rb")}
        data = {}
        if property_id:
            data["property_id"] = property_id
        return self._request("POST", "/media/upload", files=files)
