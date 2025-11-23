-- schema.sql
-- Defect lifecycle schema for SQL Server
IF OBJECT_ID('dbo.defects', 'U') IS NULL
BEGIN
CREATE TABLE dbo.defects (
    defect_id INT IDENTITY(1,1) PRIMARY KEY,
    issue_key VARCHAR(64) UNIQUE,
    summary NVARCHAR(2000),
    status VARCHAR(100),
    created DATETIME,
    resolved DATETIME,
    time_to_resolve_days FLOAT,
    priority VARCHAR(50),
    priority_score INT,
    reporter NVARCHAR(200),
    assignee NVARCHAR(200),
    issuetype VARCHAR(100),
    components NVARCHAR(500),
    labels NVARCHAR(500),
    is_open BIT,
    raw_json NVARCHAR(MAX)
);
END
