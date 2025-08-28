from pyspark.sql import SparkSession
from agent.logging_conf import logger


class POSConnector:
    def __init__(self, mcp_client):
        self.mcp = mcp_client


    def fetch(self, spark: SparkSession):
        resp = self.mcp.request("pos.read", {})
        rows = resp.get("data", {}).get("transactions", [])
        return spark.createDataFrame(rows)