load_to_sql.py
Simple ETL loader: reads cleaned CSV and writes to SQL Server using pyodbc.
"""
import pandas as pd
import pyodbc
import argparse

def get_conn(server, database, uid=None, pwd=None, trusted=True):
    if trusted:
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    else:
        conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={uid};PWD={pwd}"
    return pyodbc.connect(conn_str)

def upsert_defects(csv_path, server, database, table='defects', trusted=True, uid=None, pwd=None):
    df = pd.read_csv(csv_path, parse_dates=['created','resolved'], low_memory=False)
    conn = get_conn(server, database, uid=uid, pwd=pwd, trusted=trusted)
    cursor = conn.cursor()

    # Simple upsert: if issue_key exists, update; else insert
    for _, row in df.iterrows():
        issue_key = row.get('issue_key')
        # Check exist
        cursor.execute(f"SELECT defect_id FROM {table} WHERE issue_key = ?", issue_key)
        existing = cursor.fetchone()
        if existing:
            cursor.execute(f"""
                UPDATE {table}
                SET summary=?, status=?, created=?, resolved=?, time_to_resolve_days=?, priority=?, priority_score=?,
                    reporter=?, assignee=?, issuetype=?, components=?, labels=?, is_open=?
                WHERE issue_key=?
            """,
            row.get('summary'), row.get('status'), row.get('created'), row.get('resolved'),
            row.get('time_to_resolve_days'), row.get('priority'), row.get('priority_score'),
            row.get('reporter'), row.get('assignee'), row.get('issuetype'), row.get('components'),
            row.get('labels'), int(row.get('is_open', False)), issue_key)
        else:
            cursor.execute(f"""
                INSERT INTO {table} (issue_key, summary, status, created, resolved, time_to_resolve_days, priority, priority_score,
                    reporter, assignee, issuetype, components, labels, is_open)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            issue_key, row.get('summary'), row.get('status'), row.get('created'), row.get('resolved'),
            row.get('time_to_resolve_days'), row.get('priority'), row.get('priority_score'),
            row.get('reporter'), row.get('assignee'), row.get('issuetype'), row.get('components'),
            row.get('labels'), int(row.get('is_open', False)))
    conn.commit()
    cursor.close()
    conn.close()
    print("Upsert complete.")
