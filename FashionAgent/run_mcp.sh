#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Export environment variables (edit these with your actual secrets)
export SALESFORCE_USERNAME="your_salesforce_username"
export SALESFORCE_PASSWORD="your_salesforce_password"
export SALESFORCE_TOKEN="your_salesforce_token"
export SALESFORCE_DOMAIN="test" # 'login' for prod, 'test' for sandbox

export AZURESQL_CONN="Driver={ODBC Driver 17 for SQL Server};Server=tcp:yourserver.database.windows.net,1433;Database=yourdb;Uid=youruser;Pwd=yourpassword;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

export SNOWFLAKE_CONN="user=your_user password=your_password account=your_account warehouse=your_wh database=your_db schema=your_schema"

export SLACK_WEBHOOK="https://hooks.slack.com/services/XXX/YYY/ZZZ"

# Additional environment variables
export MCP_URL="http://localhost:8000"
export MCP_API_KEY="your_api_key" # Optional
export SF_OBJECT="Opportunity"
export EXCEL_FOLDER="/dbfs/mnt/excel_drop"
export HORIZON=28

# Start MCP server
cd mcp_server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
