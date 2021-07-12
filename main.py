from jira import JIRA
from boto3.session import Session

import logging
import config
import json
from datetime import datetime

from utils import jira_service as js
from utils import s3_service as s3s

def getCurrentDateTime():
    return datetime.today().strftime("%Y-%m-%d %H:%M")

def getFolderPathForTimeStamp():
    return datetime.today().strftime("%Y/%m/%d/%H/")

def getTimestampFilename():
    return datetime.today().strftime("%H_%M")

def recordMasterIssuesToS3():
    dateTime = getCurrentDateTime()

    logging.info("Running Master Run : Till :: " + dateTime)
    startAt = 0
    limit = 100
    i = 1
    while True:
        issues = js.getMasterIssues(dateTime,startAt,limit)
        if (len(issues) == 0):
            break
        issuesLength = issues.total
        for issue in issues:
            logging.info("Writing issue : (" + str(i) + "/" + str(issuesLength) + ") : " + str(issue))
            i = i+1
            s3s.writeToMaster(issue)
            #print(issue.raw)
        startAt = i-1
    s3s.updateLastRunFile(dateTime)

def recordIncrementalIssuesToS3():
    fromDateBinary = s3s.getLastRunFile()
    fromDate = fromDateBinary.decode("utf-8");
    #fromDate = '2021-07-09 19:00'
    tillDate = getCurrentDateTime()

    logging.info("Running Incremental Run : From :: " + fromDate + " :: To :: " + tillDate)
    jsonval = [];
    startAt = 0
    limit = 100
    i = 1
    issuesLength = 0
    while True:
        issues = js.getIncrementalIssues(fromDate, tillDate,startAt,limit)
        if (len(issues) == 0):
            logging.info("No records to write")
            break
        issuesLength = issues.total
        for issue in issues:
            logging.info("Recording issue : (" + str(i) + "/" + str(issuesLength) + ") : " + str(issue))
            i = i+1
            jsonval.append(issue.raw)
            #print(issue.raw)
        startAt = i-1
    s3s.writeToIncremental(getFolderPathForTimeStamp(), getTimestampFilename(), jsonval)
    s3s.updateLastRunFile(tillDate)

def main():
    logging.basicConfig(filename=config.general.log_location,
                        format=config.general.log_format,
                        level=config.general.log_level)
    logging.info('Run Started')
    masterFolderExists = s3s.checkMasterFolderExists()
    logging.info("Master folder exists : " + str(masterFolderExists))
    if (masterFolderExists):
        #recordMasterIssuesToS3()
        #s3s.getBucketInfo()
        recordIncrementalIssuesToS3()
    else:
        recordMasterIssuesToS3()
    logging.info('Run Ended')

if __name__ == "__main__":
    main()
