import boto3
from pprint import pprint
session=boto3.Session(profile_name='default', region_name='us-east-1')

client=boto3.client('ec2')

#create a dictionary to call the vloume id as a value.

temp_dict={
    'key1':'vol-095f44fc9aa367063'
}

successful_snapshot={}
for snapshot in temp_dict:
    print(temp_dict[snapshot])

    try:
        response=client.create_snapshot(

            Description='this is a test snapshot',
            VolumeId=temp_dict[snapshot],
            TagSpecifications=[
        {'ResourceType':'snapshot',
            'Tags': [
                {
                    'Key': 'Testing_Snapshot',
                    'Value': 'i-086e7c44607d1fdef'
                },
                {
                    'Key': 'TestEnvironment',
                    'Value': 'PythonScripting'
                }
            ]
        }]
        )
        pprint( response['ResponseMetadata'])
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        snapshot_id = response['SnapshotId']
        # check if status_code was 200 or not to ensure the snapshot was created successfully
        if status_code == 200:
            successful_snapshot[snapshot] = snapshot_id
    except Exception as e:
        exception_message = "There was error in creating snapshot " + snapshot + " with volume id "+volumes_dict[snapshot]+" and error is: \n"\
                            + str()
        print(exception_message)
# print the snapshots which were created successfully
print(successful_snapshot)