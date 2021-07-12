class JiraSettings():
    server_url = "https://humanmanaged.atlassian.net"
    user = "integration@humanmanaged.com"
    api_token = "T1tsbVLfIFE4ZLc8ojJz2C93"
    project_code = "BRVM"
    issue_type = "Vulnerability"

class S3Settings():
    access_key = "AKIAZTHLLAARHCPNXVYM"
    secret_key = "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"
    bucket_name = "bladerunner-jira-alerts"
    lastrun_file = "lastrun.txt"
    master_folder_path = "vulnerability/master/"
    incremental_folder_path = "vulnerability/incremental/"

jira = JiraSettings()
s3 = S3Settings()
