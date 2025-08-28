
import requests
from agent.logging_conf import logger


class MCPClient:
    def __init__(self, base_url: str, api_key: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key


    def request(self, tool: str, payload: dict) -> dict:
        url = f"{self.base_url}/tool/{tool}"
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        logger.info(f"MCP REQUEST -> {tool} payload_keys={list(payload.keys())}")
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()