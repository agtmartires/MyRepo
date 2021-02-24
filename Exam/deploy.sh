#!/usr/bin/bash

if [ ${#@} == 0 ]
then
    echo "No parameter entered"
    echo "Usage: ./deploy.sh create|delete"
    exit
fi

if [ $1 == "create" ]
then

# Create key for AWS
pubKeyFile="key/id_rsa.pub"
if ! test -f "$pubKeyFile"
then
    rm -rf key;mkdir key
    echo "Will create key pair for AWS"
    ssh-keygen -t rsa -f key/id_rsa

    if ! test -f "$pubKeyFile"
    then
        echo "Failed creating $pubKeyFile!"
        exit
    fi
fi

echo "Creating AWS resources and instance... Please wait."
rm -rf .resources

# upload key to AWS
ansible-playbook -v create_ec2_resources.yml --extra-vars "fileLocation=$pubKeyFile" >& .tmp

result=$(cat .tmp | grep "failed=0")
if [ "${#result}" -eq 0 ]
then
    echo -e "One of the Ansible tasks failed. Will terminate the script now."
    cat .tmp
    exit
fi

# give time to wait for instance to run
sleep 30
echo "AWS EC2 instance created"

# parse results and save details to .resources
python parse_result.py .tmp

# Connect to newly created instance and run commands in commands.sh
privateKey="key/id_rsa"
instanceId=$(cut -d " " -f 2 .resources)
ipAdd=$(cut -d " " -f 4 .resources)

cp -rf commands.sh.orig commands.sh
sed -i 's/_INSTANCE_ID_/'$instanceId'/' commands.sh

echo "PRIVATE KEY:  $privateKey"
chmod 400 $privateKey
ssh -i $privateKey  ubuntu@$ipAdd < commands.sh

echo -e "Webserver running. Check http://$ipAdd"

elif [ $1 == "delete" ]
then
    if ! test -f ".resources"
    then
        echo "No resources created yet or already deleted. No need for cleanup."
        exit
    fi

    vpcId=$(cut -d " " -f 1 .resources)
    instanceId=$(cut -d " " -f 2 .resources)
    routeTableId=$(cut -d " " -f 3 .resources)
    ipAdd=$(cut -d " " -f 4 .resources)

    echo "Resources to be deleted:"
    echo "VPC ID:         $vpcId"
    echo "Instance ID:    $instanceId"
    echo "Route Table ID: $routeTableId"
    echo "EC2 IP Add:     $ipAdd"
    echo "Deleting AWS resources... Please wait."

    ansible-playbook -v delete_ec2_resources.yml --extra-vars "vpc_id=$vpcId instance_id=$instanceId rt_id=$routeTableId" >& .tmp
    result=$(cat .tmp | grep "failed=0")
    if [ "${#result}" -eq 0 ]
    then
        echo -e "One of the Ansible tasks failed in deleting resources. "
        cat .tmp
    exit
fi
    echo "Deleted resources."
    rm -rf .resources
else
    echo "Invalid input"
    echo "Usage: ./deploy.sh create|delete"
    exit
fi


