from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()


class ToolRequest(BaseModel):
    params: Dict[str, Any]


@app.post("/tool/{tool_name}")
async def tool_exec(tool_name: str, payload: ToolRequest):
    # VERY simple mocked endpoints; extend to call real APIs
    if tool_name == 'social.trends':
        return {"data": {"trends": [{"hashtag":"#sneakers","score":0.9}]}}
    if tool_name == 'pos.read':
        return {"data": {"transactions": [{"date":"2025-01-01","units":10}]}}
    return {"data": {}}
