from __future__ import annotations
import os
from pydantic import BaseModel, Field


class MCPConfig(BaseModel):
    url: str = Field(...)
    api_key: str | None = None


class SourcesConfig(BaseModel):
    salesforce_object: str = Field("Opportunity")
    excel_folder: str = Field("/dbfs/mnt/excel_drop")
    azuresql_conn: str = Field("")
    snowflake_conn: str = Field("")


class AlertsConfig(BaseModel):
    slack_webhook: str | None = None


class ModelConfig(BaseModel):
    horizon_days: int = 28
    min_history_days: int = 90


class AppConfig(BaseModel):
    env: str = Field(default=os.getenv("ENV", "dev"))
    mcp: MCPConfig
    sources: SourcesConfig
    alerts: AlertsConfig
    model: ModelConfig


    @staticmethod
    def from_env() -> "AppConfig":
        return AppConfig(
            mcp=MCPConfig(url=os.getenv("MCP_URL", "http://localhost:8000"), api_key=os.getenv("MCP_API_KEY")),
            sources=SourcesConfig(
                salesforce_object=os.getenv("SF_OBJECT", "Opportunity"),
                excel_folder=os.getenv("EXCEL_FOLDER", "/dbfs/mnt/excel_drop"),
                azuresql_conn=os.getenv("AZURESQL_CONN", ""),
                snowflake_conn=os.getenv("SNOWFLAKE_CONN", ""),
            ),
            alerts=AlertsConfig(slack_webhook=os.getenv("SLACK_WEBHOOK")),
            model=ModelConfig(horizon_days=int(os.getenv("HORIZON", "28")))
        )