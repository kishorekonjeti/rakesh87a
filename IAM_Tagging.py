import boto3
import datetime
from datetime import date
import time
import csv
from pprint import pprint
from botocore.exceptions import ClientError

client = boto3.client('iam')
users=client.list_users()['Users']

final_data_from_raw_filter = []
result = []
for user in users:
    # print(user)
    Username=user['UserName']
    AccessKeyList_Username=client.list_access_keys(UserName=Username)
    raw_data=AccessKeyList_Username['AccessKeyMetadata']
    final_data_from_raw_filter.append(raw_data)

#print(final_data_from_raw_filter)

for each_list in final_data_from_raw_filter:
    for each in each_list:
        result.append(each['UserName'])

#print(result)

with open("C:/Temp/iam_tagging.csv", newline='') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
#        print(row)
        for each_user in users:
            if each_user['UserName'] == row['Iam_Username']:
#                print(row['Iam_Username'], row['E-Mail'], row['E-Mail_Value'], row['ServiceAccount'])
#                Tags_var={row['E-Mail']:row['E-Mail_Value'], row['ServiceAccount']:row['ServiceAccount_Value'], row['Owner']:row['Owner_Value']}
                response = client.tag_user(
                    UserName=row['Iam_Username'], Tags = [
                    {
                        'Key': row['E-Mail'],
                        "Value": row['E-Mail_Value']
                    },
                    {
                        'Key': row['ServiceAccount'],
                        "Value": row['ServiceAccount_Value']
                    },
                    {
                        'Key': row['Owner'],
                        "Value": row['Owner_Value']
                    },
                    {
                        'Key': row['Environment'],
                        "Value": row['Environment_Value']
                    },
                    {
                        'Key': row['EngineerContact'],
                        "Value": row['EngineerContact_Value']
                    },
                    {
                        'Key': row['EngineeringTeam'],
                        "Value": row['EngineeringTeam_Value']
                    }
                ]
                )
                print("Tags Applied for the user account:", row['Iam_Username'])