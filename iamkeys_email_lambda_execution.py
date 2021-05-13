# PCS standard.(Security policy).   More tahn 90 days password change 
# inactive aws account in in active for more than 60 days.
# time_difference1: 76- 90 th  mail has to sent
# time_difference2: 90 days mail trigger account inactive

import boto3
import datetime
from datetime import date
import time
import csv
from pprint import pprint
from botocore.exceptions import ClientError

email_list=[]

#inactive_users_dic={}

def lambda_handler(event,context):

    client = boto3.client('iam')
    users=client.list_users()['Users']
    
    count=0
    
    for user in users:
        count=count+1
    #    print(user['UserName'])
        Username=user['UserName']
        AccessKeyList_Username=client.list_access_keys(UserName=Username)
    #    print(count, AccessKeyList_Username['AccessKeyMetadata'])
        raw_data=AccessKeyList_Username['AccessKeyMetadata']
        print(raw_data)
        
        User_Access_Key = ""
        User_Name = ""
        User_Status = ""
        User_EMail = ""
    counter = 1
    for data in raw_data:
        print("counter: {}".format(counter))
        counter = counter + 1
        User_Access_Key = data['AccessKeyId']
        User_Name = data['UserName']
        User_Status = data['Status']
        UserTags_List = client.list_user_tags(UserName=data['UserName'])['Tags']
        for tag_filter in UserTags_List:         
            if (tag_filter['Key'] == 'E-Mail'):                
                User_EMail = tag_filter['Value']
                email_list.append(User_EMail)
                print("User_EMail: {}".format(User_EMail))
                print("User_Name: {}".format(User_Name))
                if (User_Name == 'rakuluru' or User_Name == 'ansible'):
                    print("Execution for AccessKeyAge Check")
                    current_date = date.today()
                    access_key_age = current_date - data['CreateDate'].date()
                    time_difference1=datetime.timedelta(days=225)
                    time_difference2=datetime.timedelta(days=230)
                    print("first condition {}".format(access_key_age >= time_difference1))
                    print("second condition {}".format(access_key_age <= time_difference2))
                    if (access_key_age >= time_difference1 or access_key_age <= time_difference2):
                        send_email(User_Access_Key, User_Name, email_list)
                    else:
                        print("time difference condition not met.")
                else:
                    print("user is not rakuluru or ansible")
            else:
                print("E-Mail Id is not exist for this user:", User_Name)

def send_email(User_Access_Key, User_Name, email_list):
    print("User_Access_Key: {}".format(User_Access_Key))
    print("User_Name: {}".format(User_Name))
    print("email_list: {}".format(email_list))
    email_unique = list(set(email_list))
    print(email_unique)
    RECIPIENTS = email_unique
    SENDER = "awsiamaccounts@frontdoorhome.com"
    AWS_REGION = 'us-east-1'
    SUBJECT = "IAM Access Key Rotation"
    BODY_TEXT = ("Your IAM Access Key need to be rotated in AWS Account: 056079971884 as it is 3 months or older.\r\n"
                "Log into AWS and go to your IAM user to fix: https://console.aws.amazon.com/iam/home?#security_credential")            
    BODY_HTML = """Your IAM Access Key need to be rotated in AWS AHSVDI Account: 154112709229 as it is 3 months or older.\r\n
                                Log into AWS and go to your IAM user to fix: https://ahsvdi.signin.aws.amazon.com/console \r\n
                                AccessKey = {0}, Username = {1}""".format(User_Access_Key,User_Name)
    CHARSET = "UTF-8"
    session=boto3.Session(region_name='us-east-1')
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': RECIPIENTS,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
