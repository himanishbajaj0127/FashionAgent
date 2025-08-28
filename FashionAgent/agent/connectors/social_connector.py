from pyspark.sql import SparkSession
from agent.logging_conf import logger


class SocialConnector:
    def __init__(self, mcp_client):
        self.mcp = mcp_client


    def fetch(self, spark: SparkSession):
        resp = self.mcp.request("social.trends", {"platforms": ["instagram", "tiktok"]})
        rows = resp.get("data", {}).get("trends", [])
        return spark.createDataFrame(rows)
