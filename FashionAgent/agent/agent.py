from pyspark.sql import SparkSession
from agent.config import AppConfig
from agent.mcp_client import MCPClient
from agent.connectors.salesforce_connector import SalesforceConnector
from agent.connectors.excel_connector import ExcelConnector
from agent.connectors.azuresql_connector import AzureSQLConnector
from agent.connectors.snowflake_connector import SnowflakeConnector
from agent.connectors.social_connector import SocialConnector
from agent.connectors.pos_connector import POSConnector
from agent.forecasting.features import build_training_frame
from agent.forecasting.model import DemandModel
from agent.actions.alerts import AlertEngine
from agent.logging_conf import logger
import pandas as pd


class FashionAgent:
    def __init__(self, spark: SparkSession, cfg: AppConfig):
        self.spark = spark
        self.cfg = cfg
        self.mcp = MCPClient(cfg.mcp.url, cfg.mcp.api_key)
        self.alerts = AlertEngine(cfg.alerts.slack_webhook)
        # connectors (Salesforce requires credentials passed separately)
        self.sf = None
        self.excel = ExcelConnector(cfg.sources.excel_folder)
        self.azuresql = AzureSQLConnector(cfg.sources.azuresql_conn) if cfg.sources.azuresql_conn else None
        self.snowflake = SnowflakeConnector({}) if cfg.sources.snowflake_conn else None
        self.social = SocialConnector(self.mcp)
        self.pos = POSConnector(self.mcp)
        self.model = DemandModel(cfg.model.horizon_days)

    def ingest(self, spark: SparkSession):
        logger.info("Starting ingestion...")
        dfs = {}
        try:
            dfs['excel'] = self.excel.fetch(spark)
        except Exception as e:
            logger.info(f"Excel ingest failed: {e}")
            dfs['excel'] = None
        try:
            if self.azuresql:
                dfs['azuresql'] = self.azuresql.fetch(spark, "SELECT date, units, sku, region FROM sales;")
        except Exception as e:
            logger.info(f"Azure SQL ingest failed: {e}")
            dfs['azuresql'] = None
        try:
            dfs['pos'] = self.pos.fetch(spark)
        except Exception as e:
            logger.info(f"POS ingest failed: {e}")
            dfs['pos'] = None
        try:
            dfs['social'] = self.social.fetch(spark)
        except Exception as e:
            logger.info(f"Social ingest failed: {e}")
            dfs['social'] = None
        return dfs

    def build_timeseries(self, dfs) -> pd.DataFrame:
        # Simple union of sources into a pandas timeseries for demo
        frames = []
        for k, df in dfs.items():
            if df is None:
                continue
            try:
                pdf = df.select('date', 'units').toPandas()
                frames.append(pdf)
            except Exception:
                continue
        if not frames:
            return pd.DataFrame()
        all_df = pd.concat(frames)
        all_df.columns = ['date', 'units']
        all_df = all_df.dropna()
        return all_df

    def run_forecast_and_alert(self, ts_df: pd.DataFrame):
        if ts_df.empty:
            logger.info("No timeseries data; skipping forecast")
            return None
        train = build_training_frame(ts_df)
        if len(train) < self.cfg.model.min_history_days:
            logger.info("Not enough history for model")
            return None
        fc = self.model.fit_predict(train)
        # Basic risk detection
        last = fc.tail(7)
        mean = last['yhat'].mean()
        if mean < 1:
            self.alerts.post_slack("Low forecasted demand detected for some SKUs")
        return fc
