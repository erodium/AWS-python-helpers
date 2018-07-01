import boto3
from pprint import pprint

client = boto3.client('ec2') #set up the EC2 client

runningInstances = [] #placeholder for a list of instances that are running

#get a list of all the regions
regions = [region['RegionName'] for region in client.describe_regions()['Regions']]


for region in regions: #for each region
    client = boto3.client('ec2', region_name=region) #set up a link to EC2 within that region
    response = client.describe_instance_status() #find all the running instances
    for status in response['InstanceStatuses']: #for each running instance in the region
        if 'InstanceId' in status.keys(): #status could be empty if there are no running instances
            runningInstances.append(status['InstanceId']) #for each running instance, append the ID
    if runningInstances: #runningInstances could be empty if there are no running instances in the region
        response = client.stop_instances(
            InstanceIds=runningInstances
        ) #stop the instance
        for action in response['StoppingInstances']:
            pprint("Stopping Instance " + action['InstanceId'] + " in region " + region)