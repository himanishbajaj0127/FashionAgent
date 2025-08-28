from pyspark.sql import SparkSession
from agent.logging_conf import logger


class ExcelConnector:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path


    def fetch(self, spark: SparkSession):
        logger.info(f"Reading Excel files from {self.folder_path}")
        df = spark.read.format("com.crealytics.spark.excel").option("useHeader", "true").load(self.folder_path)
        return df