import logging

class JiraSettings():
    server_url = "https://humanmanaged.atlassian.net"
    user = "integration@humanmanaged.com"
    api_token = "<api_token>"
    project_code = "BRVM"
    issue_type = "Vulnerability"

class S3Settings():
    access_key = "<access_key>"
    secret_key = "<secret_key>"
    bucket_name = "bladerunner-jira-alerts"
    lastrun_file = "lastrun.txt"
    master_folder_path = "vulnerability/master/"
    incremental_folder_path = "vulnerability/incremental/"

class GeneralSettings():
    log_location = "/tmp/jira2s3.log"
    log_format = '%(asctime)s :: %(levelname)s :: %(message)s'
    log_level = logging.INFO

jira = JiraSettings()
s3 = S3Settings()
general = GeneralSettings()
