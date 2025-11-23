"""
jira_parser.py
Parse JIRA export (CSV or JSON), normalize defect lifecycle fields, and save as clean CSV / push to SQL Server.
"""
import os
import json
import pandas as pd
import datetime
import argparse

def load_jira_csv(path):
    df = pd.read_csv(path, low_memory=False)
    return df

def load_jira_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # If it's JIRA API results, adapt to issues list
    issues = data.get('issues', data)
    rows = []
    for issue in issues:
        key = issue.get('key') or issue.get('id')
        fields = issue.get('fields', {})
        rows.append({
            'issue_key': key,
            'summary': fields.get('summary'),
            'status': fields.get('status', {}).get('name') if fields.get('status') else None,
            'created': fields.get('created'),
            'resolved': fields.get('resolutiondate') or fields.get('resolved'),
            'priority': fields.get('priority', {}).get('name') if fields.get('priority') else None,
            'reporter': fields.get('reporter', {}).get('displayName') if fields.get('reporter') else None,
            'assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else None,
            'issuetype': fields.get('issuetype', {}).get('name') if fields.get('issuetype') else None,
            'components': ','.join([c.get('name') for c in fields.get('components', [])]) if fields.get('components') else None,
            'labels': ','.join(fields.get('labels')) if fields.get('labels') else None,
            'priority_score': None
        })
    return pd.DataFrame(rows)

def normalize_dates(df, date_cols=['created','resolved']):
    for c in date_cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors='coerce')
    return df

def compute_lifecycle_metrics(df):
    # Time to resolve
    df['time_to_resolve_days'] = (df['resolved'] - df['created']).dt.total_seconds() / 86400.0
    # Fill or mark open issues
    df['is_open'] = df['resolved'].isna()
    return df

def priority_to_score(priority):
    mapping = {'Highest':5, 'High':4, 'Medium':3, 'Low':2, 'Lowest':1}
    return mapping.get(priority, 0)

def enrich_priority(df):
    if 'priority' in df.columns:
        df['priority_score'] = df['priority'].apply(priority_to_score)
    return df

def main(args):
    input_path = args.input
    out_csv = args.out or 'clean_jira_defects.csv'
    fmt = 'csv' if input_path.lower().endswith('.csv') else 'json'
    if fmt == 'csv':
        df = load_jira_csv(input_path)
    else:
        df = load_jira_json(input_path)

    # Common transformations - adapt column names as necessary
    # Try to map common JIRA column names
    # If JIRA CSV has 'Issue key' or 'Key'
    if 'Issue key' in df.columns and 'issue_key' not in df.columns:
        df = df.rename(columns={'Issue key':'issue_key'})
    if 'Key' in df.columns and 'issue_key' not in df.columns:
        df = df.rename(columns={'Key':'issue_key'})
    # Map created/resolved/resolutiondate
    if 'Created' in df.columns and 'created' not in df.columns:
        df = df.rename(columns={'Created':'created'})
    if 'Resolved' in df.columns and 'resolved' not in df.columns:
        df = df.rename(columns={'Resolved':'resolved'})
    if 'Resolutiondate' in df.columns and 'resolved' not in df.columns:
        df = df.rename(columns={'Resolutiondate':'resolved'})
    if 'Status' in df.columns and 'status' not in df.columns:
        df = df.rename(columns={'Status':'status'})
    if 'Priority' in df.columns and 'priority' not in df.columns:
        df = df.rename(columns={'Priority':'priority'})

    # Normalize
    df = normalize_dates(df, date_cols=['created','resolved'])
    df = compute_lifecycle_metrics(df)
    df = enrich_priority(df)

    # Export clean CSV
    df.to_csv(out_csv, index=False)
    print(f"Clean defects exported to {out_csv}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse JIRA exports and normalize defect lifecycle data.')
    parser.add_argument('--input', '-i', required=True, help='Path to JIRA CSV or JSON export')
    parser.add_argument('--out', '-o', required=False, help='Path to output cleaned CSV')
    args = parser.parse_args()
    main(args)
