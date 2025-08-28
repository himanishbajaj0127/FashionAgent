from simple_salesforce import Salesforce
from pyspark.sql import SparkSession
from agent.logging_conf import logger


class SalesforceConnector:
    def __init__(self, username: str, password: str, token: str, domain: str = "test"):
        self.sf = Salesforce(username=username, password=password, security_token=token, domain=domain)


    def fetch(self, query: str, spark: SparkSession):
        logger.info("Querying Salesforce sandbox...")
        res = self.sf.query_all(query)
        records = res.get("records", [])
        if not records:
            return spark.createDataFrame([], schema="id STRING")
        return spark.createDataFrame(records)
