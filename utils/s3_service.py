from boto3.session import Session

import config
import json

session = Session(aws_access_key_id=config.s3.access_key,
                  aws_secret_access_key=config.s3.secret_key)

# s3client = session.client('s3')
# result = s3client.get_bucket_acl(Bucket='bladerunner-jira-alerts')
# print(result)

def IsObjectPathExists(bucket, path):
    for object_summary in bucket.objects.filter(Prefix=path):
        return True
    return False

def checkMasterFolderExists():
    s3 = session.resource('s3')
    bucket = s3.Bucket(config.s3.bucket_name)
    return (IsObjectPathExists(bucket, config.s3.master_folder_path))

def writeToMaster(issue):
    s3 = session.resource('s3')
    filePath = config.s3.master_folder_path + issue.key + ".json";
    ret = s3.Object(config.s3.bucket_name, filePath).put(Body=json.dumps(issue.raw))
    #print(ret)

def writeToIncremental(folder, filename, issues):
    s3 = session.resource('s3')
    filePath = config.s3.incremental_folder_path + folder + filename + ".json"
    ret = s3.Object(config.s3.bucket_name, filePath).put(Body=json.dumps(issues))
    #print(ret)

def updateLastRunFile(dateTime):
    s3 = session.resource('s3')
    ret = s3.Object(config.s3.bucket_name, config.s3.lastrun_file).put(Body=dateTime)

def getLastRunFile():
    s3 = session.resource('s3')
    obj = s3.Object(config.s3.bucket_name, config.s3.lastrun_file)
    body = obj.get()['Body'].read()
    print(body)
    return body

def getBucketInfo():
    print("inside get bucket info")
    s3 = session.resource('s3')
    bucket = s3.Bucket(config.s3.bucket_name)

    print("Name: {}".format(bucket.name))
    print("Creation Date: {}".format(bucket.creation_date))
    for object in bucket.objects.all():
        print("Object: {}".format(object))

    # obj = s3.Object(config.s3.bucket_name, config.s3.lastrun_file)
    # body = obj.get()['Body'].read()
    # print(body)
    return;
