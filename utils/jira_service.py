from jira import JIRA
from datetime import datetime

import config
import logging

jira = JIRA(server=config.jira.server_url,
            basic_auth=(config.jira.user, config.jira.api_token))

def getAllIssueQuery(tillDate):
    query =  "project=" + config.jira.project_code + \
            " AND issuetype=" + config.jira.issue_type + \
            " AND updatedDate<'" + tillDate + "'"
    logging.info(query)
    return query

def getIncrementalIssueQuery(fromDate, tillDate):
    query =  "project=" + config.jira.project_code + \
            " AND issuetype=" + config.jira.issue_type + \
            " AND updatedDate>='" + fromDate + "'" + \
            " And updatedDate<='" + tillDate + "'"
    logging.info(query)
    return query

def getMasterIssues(dateTime, startAt, limit):
    #date = datetime.today().strftime('%Y-%m-%d')
    issues = jira.search_issues(jql_str=getAllIssueQuery(dateTime),startAt=startAt,maxResults=limit)
    return issues

def getIncrementalIssues(fromDate, tillDate, startAt, limit):
    issues = jira.search_issues(jql_str=getIncrementalIssueQuery(fromDate, tillDate),
                                startAt=startAt,
                                maxResults=limit)
    return issues

def getIssueRaw(issue):
    iss = jira.issue(issue)
    return iss.raw
