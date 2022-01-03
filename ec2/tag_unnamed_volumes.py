#!/usr/bin/env python3
import boto3
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_name_and_volume_id():
    """
    Generate a dictionary of volume IDs and Name tags
    :return: Returns vol_id_and_name a dictionary of volume I
    """
    try:
        client = boto3.client(
            'ec2',
            region_name='us-east-1',
            aws_access_key_id='',
            aws_secret_access_key='',
        )
        response = client.describe_instances()
        vid_name_list = []
        for r in response['Reservations']:
            vol_id_and_name = {}
            for i in r['Instances']:
                for t in i['Tags']:
                    if t['Key'] == 'Name':
                        instance_name = (t['Value'])
                        for b in i['BlockDeviceMappings']:
                            vol_id = b['Ebs']['VolumeId']
                            vol_id_and_name.update({instance_name:vol_id})
                            vid_name_list.append(vol_id_and_name)
        return vid_name_list
    except Exception as E:
        print(E)


def tag_volumes_without_name(vol_id_and_instance_name):
    """
    Tag EBS volumes that do not have a tag Value for the Name key.
    :param vol_id_and_instance_name: Dictionary, of inst
    :return: No return value from this function
    """
    ec2 = boto3.resource(
        'ec2',
        region_name='us-east-1',
        aws_access_key_id='',
        aws_secret_access_key=''
    )
    for vol in vol_id_and_instance_name:
        vol_id = (list(vol.values()))
        inst_name = (list(vol.keys()))
        volume = ec2.Volume(vol_id[0])

        volume.create_tags(
            Tags=[
                {
                    'Key': 'Name',
                    'Value': str(inst_name[0])
                }
            ]
        )


if __name__ == '__main__':
    tag_volumes_without_name(get_name_and_volume_id())
