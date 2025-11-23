# Intelligent Defect Lifecycle Analytics & QA Dashboard
This project automates the end-to-end defect lifecycle analysis process by parsing JIRA logs, transforming them into structured datasets, storing them in SQL Server, and visualizing trends in Power BI.
It eliminates manual QA reporting and provides real-time insights into defect severity, resolution efficiency, and team performance.

## Features
Automated parsing of JIRA CSV/JSON export files
Cleansing & standardization of defect lifecycle fields
SQL Server storage with upsert logic
Calculation of metrics such as:
Time to resolve (TTR)
Severity/priority scoring
Open vs closed defects
Interactive Power BI dashboards
DAX measures for actionable QA insights
Supports STLC defect analysis for QA teams

### Project Structure
/Intelligent-Defect-Analytics
│
├── jira_parser.py          # Parses JIRA CSV/JSON files and normalizes lifecycle data
├── etl_load_to_sql.py      # Loads cleaned defects → SQL Server (with UPSERT logic)
├── db_schema.sql           # Database schema for defect lifecycle
├── powerbi_README.md       # Power BI setup + DAX formulas
├── requirements.txt        # Python package dependencies
└── README.md               # Main documentation

#### How It Works
# 1. JIRA Export Parsing
Reads JIRA CSV or JSON
Extracts defect fields
Normalizes timestamps and statuses
Computes lifecycle metrics (TTR, open/closed)
## 2. ETL Pipeline (Python → SQL Server)
Loads cleaned CSV
UPSERT logic maintains unique defect entries
Supports Windows Auth or SQL Auth
### 3. Power BI Dashboard
Visualizes:
Defects by priority
Defects opened vs closed trend
Average resolution time
SLA breaches
Team workload
Component-wise defect distribution

##### Setup Instructions
Install dependencies
pip install -r requirements.txt
Parse JIRA export
python jira_parser.py --input JIRA_export.csv --out clean_defects.csv
Load data into SQL Server
python etl_load_to_sql.py --csv clean_defects.csv --server YOUR_SERVER --database YOUR_DB --trusted True
Build Power BI Dashboard
Open powerbi_README.md for visuals & DAX formulas.

###### Example Metrics
Average Resolution Time: 2.9 days
SLA Breach Rate: 14.7%
Most Frequent Issue Type: Bug
Peak Defect Period: Week 32

###### Technologies Used
Python (Pandas, PyODBC)
SQL Server
Power BI
DAX
JIRA (CSV/JSON export)

###### LIPSA PATTANAIK | ITER SOA UNIVERSITY
