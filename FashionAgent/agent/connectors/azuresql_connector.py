from sqlalchemy import create_engine
from pyspark.sql import SparkSession
from agent.logging_conf import logger
import pandas as pd


class AzureSQLConnector:
    def __init__(self, conn_str: str):
        self.conn_str = conn_str
        self.engine = create_engine(conn_str)


    def fetch(self, spark: SparkSession, query: str):
        logger.info("Querying Azure SQL...")
        df = pd.read_sql_query(query, self.engine)
        return spark.createDataFrame(df)
