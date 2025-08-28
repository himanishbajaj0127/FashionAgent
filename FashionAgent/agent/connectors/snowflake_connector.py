import snowflake.connector
from pyspark.sql import SparkSession
from agent.logging_conf import logger
import pandas as pd


class SnowflakeConnector:
    def __init__(self, conn_params: dict):
        self.params = conn_params


    def fetch(self, spark: SparkSession, sql: str):
        logger.info("Querying Snowflake...")
        ctx = snowflake.connector.connect(**self.params)
        cur = ctx.cursor()
        cur.execute(sql)
        cols = [c[0] for c in cur.description]
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=cols)
        cur.close()
        ctx.close()
        return spark.createDataFrame(df)
