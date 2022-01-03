#!/usr/bin/env python3
import boto3
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_available_volumes():
    """
    List all available EBS volumes for a given AWS region
    :return: type=list, Returns a list of EBS volume IDs, filtered by availability
    """
    try:
        ec2 = boto3.resource(
            'ec2',
            region_name='us-east-1',
            aws_access_key_id='',
            aws_secret_access_key=''
                             )
        volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])
        volume_ids = [v.id for v in volumes]
        return volume_ids
    except Exception as E:
        print(E)


def delete_available_volumes(volumes):
    """
    Iterate over a list of volumes and delete them
    :param volumes: type=list, List of volume ID's to delete
    :return: returns nothing
    """
    try:
        ec2 = boto3.resource(
            'ec2',
            region_name='us-east-1',
            aws_access_key_id='',
            aws_secret_access_key=''
        )
        for v in volumes:
            volume = ec2.Volume(str(v))
            volume.delete()
    except Exception as E:
        print(E)


if __name__ == '__main__':
    delete_available_volumes(get_available_volumes())
