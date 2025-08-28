# FashionAgent: AI-Powered Fashion Retail Forecasting

## 📖 Introduction
FashionAgent is an AI-driven solution designed to enhance forecasting and decision-making in the fashion retail industry. By integrating various data sources, it provides actionable insights to optimize inventory management and sales strategies.

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/FashionAgent.git
cd FashionAgent_HybridSetup_Prod_Repo
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Edit `run_mcp.sh` to set your Salesforce, Azure SQL, Snowflake, and Slack credentials. The script includes placeholders for the following environment variables:
- `SALESFORCE_USERNAME`: Your Salesforce username
- `SALESFORCE_PASSWORD`: Your Salesforce password
- `SALESFORCE_TOKEN`: Your Salesforce security token
- `AZURESQL_CONN`: Your Azure SQL connection string
- `SNOWFLAKE_CONN`: Your Snowflake connection string (format: "user=username password=password account=account warehouse=warehouse database=database schema=schema")
- `SLACK_WEBHOOK`: Your Slack webhook URL
- `MCP_URL`: MCP server URL (default: "http://localhost:8000")
- `MCP_API_KEY`: Optional API key for MCP authentication
- `SF_OBJECT`: Salesforce object to query (default: "Opportunity")
- `EXCEL_FOLDER`: Path to Excel files (default: "/dbfs/mnt/excel_drop")
- `HORIZON`: Forecast horizon in days (default: 28)

### 4. Run the MCP Server
```bash
bash run_mcp.sh
```
This will start a FastAPI MCP server at `http://localhost:8000`.

### 5. Upload to Databricks
- Go to [Databricks CE](https://community.cloud.databricks.com/)
- Create a cluster (Python 3.x, small node)
- Import `orchestrator.py`
- Attach `requirements.txt` as a library
- Run the job

### 6. View Forecasts & Alerts
- Forecast outputs are stored in Delta tables (Databricks).
- Slack alerts are sent to the configured channel.

---

## 📊 Example Workflow
1. Fetch CRM data from Salesforce Sandbox.
2. Load inventory sheets from Excel (Google Drive/local).
3. Query sales transactions from Azure SQL.
4. Fetch warehouse stock from Snowflake.
5. Merge data into a single feature store.
6. Run `demand_forecaster.py` to predict demand.
7. Compare demand vs. stock.
8. Trigger a Slack alert if stock shortage is predicted.

---

## 🧑‍💻 Tech Stack
- **Databricks** (Spark Orchestration)
- **MCP Protocol** (local FastAPI server)
- **Salesforce Sandbox** (CRM)
- **Azure SQL, Snowflake, Excel** (data sources)
- **PySpark, Pandas, MLlib** (forecasting)
- **Slack API** (alerts)

---

## 📌 Next Steps
- Extend MCP to support tool manifests for external apps.
- Add real-time API triggers instead of batch processing.
- Deploy the MCP server on Azure App Service for scalability.

---

✅ With this setup, you can demo an enterprise-grade AI Agent that resonates with fashion industry recruiters and product-based companies.

---

## 📁 Project Structure

```
FashionAgent/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── agent/                    # Main agent module
│   ├── agent.py             # Main agent class and logic
│   ├── config.py            # Configuration management
│   ├── logging_conf.py      # Logging configuration
│   ├── mcp_client.py        # MCP client implementation
│   ├── orchestrator.py      # Workflow orchestration
│   ├── actions/             # Action handlers
│   │   └── alert.py         # Alert generation and handling
│   ├── connectors/          # Data source connectors
│   │   ├── __init__.py
│   │   ├── azuresql_connector.py    # Azure SQL connector
│   │   ├── excel_connector.py       # Excel file connector
│   │   ├── pos_connector.py         # POS system connector
│   │   ├── salesforce_connector.py  # Salesforce CRM connector
│   │   ├── snowflake_connector.py   # Snowflake data warehouse connector
│   │   └── social_connector.py      # Social media data connector
│   └── forecasting/         # Forecasting module
│       ├── __init__.py
│       ├── features.py      # Feature engineering
│       └── model.py         # ML model implementation
└── mcp_server/              # MCP server implementation
    └── app.py               # FastAPI MCP server application
```

This structure organizes the code into logical modules:
- **agent/**: Core AI agent functionality
- **connectors/**: Data source integrations
- **forecasting/**: Machine learning and prediction logic
- **mcp_server/**: Model Context Protocol server
- **actions/**: Specific action implementations
