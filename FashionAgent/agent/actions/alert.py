import requests
from agent.logging_conf import logger


class AlertEngine:
    def __init__(self, slack_webhook: str | None):
        self.slack_webhook = slack_webhook


    def post_slack(self, text: str):
        if not self.slack_webhook:
            logger.info("No slack webhook configured; skipping slack post")
            return
        payload = {"text": text}
        resp = requests.post(self.slack_webhook, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info("Posted alert to Slack")