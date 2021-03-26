import boto3
import datetime
from datetime import date
import time
import csv
from pprint import pprint
from botocore.exceptions import ClientError

client = boto3.client('iam')
users=client.list_users()['Users']

count=0
inactive_users_dic={}

email_list=[]
Final_Accounts=[]

exception_list = ['aceyus_reporting_test', 'ahs-contractpdf-test',]

for user in users:
    count=count+1
    Username=user['UserName']
    AccessKeyList_Username_1=client.list_access_keys(UserName=Username)
    raw_data=AccessKeyList_Username_1['AccessKeyMetadata']
    # print(raw_data)

    for data in raw_data:
#        print (data['UserName'], data['AccessKeyId'], data['Status'])
        if data['Status'] == 'Active':
            Final_Accounts.append(data['UserName'])
# print(Final_Accounts)
for each_element in exception_list:
    if each_element in Final_Accounts:
        Final_Accounts.remove(each_element)

# print(Final_Accounts) #It prints after removing accounts from Exception list, it get stored only final accounts

for each_user in Final_Accounts:
    AccessKeyList_Username_2=client.list_access_keys(UserName=each_user)
    Final_Data = AccessKeyList_Username_2['AccessKeyMetadata']
    # print(Final_Data)

    for user_data in Final_Data:
        if user_data['Status'] == 'Active':
            current_date = date.today()
            access_key_age = current_date - user_data['CreateDate'].date()
            # print('Username:', user_data['UserName'], 'Total AccessKeyAge:', access_key_age ,'Status:', user_data['Status'])
            time_difference1=datetime.timedelta(days=76)
            time_difference2=datetime.timedelta(days=90)
            time_difference3=datetime.timedelta(days=90)
            if (access_key_age > time_difference1) and (access_key_age <= time_difference2):
                print('Username:', user_data['UserName'], 'Total AccessKeyAge:', access_key_age ,'Status:', user_data['Status'])
                UserTags_List = client.list_user_tags(UserName=user_data['UserName'])['Tags']
#                print(UserTags_List)
                for tag_filter in UserTags_List:
                    if (tag_filter['Key']) == 'E-Mail':
                        email_list.append(tag_filter['Value'])
#print(email_list)
            if (access_key_age > time_difference3):
                print('Username:', user_data['UserName'], 'Total AccessKeyAge:', access_key_age ,'Status:', user_data['Status'])
                inactive_users_dic[user_data['UserName']] = user_data['AccessKeyId']
                client.update_access_key(UserName=user_data['UserName'], AccessKeyId=data['AccessKeyId'], Status='Inactive')
                print('User set into InActive State:', user_data['UserName'])

#From Above program got the output list of users Access KeyAge from 81st day to 95th day, all users mail addresses are listed in above e-mail list with this sending output below                       
email_unique = list(set(email_list))
print(email_unique)
RECIPIENTS = email_unique
SENDER = "awsiamaccounts@frontdoorhome.com"
AWS_REGION = 'us-east-1'
SUBJECT = "IAM Access Key Rotation"
BODY_TEXT = ("Your IAM Access Key need to be rotated in AWS AHS-TEST Account: 544565394617 as it is 3 months or older.\r\n"
            "Log into AWS and go to your IAM user to fix: https://ahstest.signin.aws.amazon.com/console")            
BODY_HTML = """
AWS Security: IAM Access Key Rotation: Your IAM Access Key need to be rotated in <b>AWS AHS-TEST Account: 544565394617 as it is 3 months or older.</b> <br>Log into AWS and go to your <a href="https://console.aws.amazon.com/iam/home?#security_credential">please click here</a>  to create a new set of keys. Ensure to disable / remove your previous key pair.
            """           
CHARSET = "UTF-8"
session=boto3.Session(profile_name='AHSTEST',region_name='us-east-1')
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
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])