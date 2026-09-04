import re
import httpx

ID = re.compile(r"^[A-Za-z0-9_-]+$")

class Trestle:
    def __init__(self, base: str, token: str, transport=None):
        self.base = base.rstrip("/")
        self.token = token
        self.transport = transport

    async def request(self, path: str, method: str = "GET", json=None):
        headers = {"accept": "application/json"}
        if self.token:
            headers["authorization"] = f"Bearer {self.token}"
        async with httpx.AsyncClient(base_url=self.base, headers=headers, transport=self.transport, timeout=10, trust_env=False) as client:
            response = await client.request(method, path, json=json)
        try:
            data = response.json()
        except ValueError:
            data = {}
        if response.is_error:
            message = data.get("error", {}).get("message", "Trestle request failed")
            raise RuntimeError(message)
        return data

def observation_path(record_id: str = "") -> str:
    if record_id and not ID.fullmatch(record_id):
        raise ValueError("invalid observation id")
    suffix = f"/{record_id}" if record_id else ""
    return f"/api/v1/collections/fn_observations/records{suffix}"
