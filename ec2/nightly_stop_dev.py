import json
import boto3


def lambda_handler(event, context):
    try:
        ec2 = boto3.client(
            'ec2',
            region_name='us-east-1'
        )
        response = ec2.describe_instances(
            Filters=[
                {'Name': 'tag:Dev',
                 'Values': ['True']}
            ]).get('Reservations', [])
        instances = []
        for i in range(len(response)):
            for x in response[i]['Instances']:
                instances.append(x['InstanceId'])
        ec2.stop_instances(InstanceIds=instances)
    except Exception as e:
        print(e)
