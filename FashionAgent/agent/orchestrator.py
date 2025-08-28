from pyspark.sql import SparkSession
from agent.config import AppConfig
from agent.agent import FashionAgent
from agent.logging_conf import logger


def main():
    cfg = AppConfig.from_env()
    spark = SparkSession.builder.appName("FashionAgentHybrid").getOrCreate()
    agent = FashionAgent(spark, cfg)
    dfs = agent.ingest(spark)
    ts = agent.build_timeseries(dfs)
    fc = agent.run_forecast_and_alert(ts)
    if fc is not None:
        logger.info("Forecast completed; writing to /dbfs/FileStore/fashion/forecast.csv")
        import os
        os.makedirs('/dbfs/FileStore/fashion', exist_ok=True)
        fc.to_csv('/dbfs/FileStore/fashion/forecast.csv', index=False)


if __name__ == '__main__':
    main()