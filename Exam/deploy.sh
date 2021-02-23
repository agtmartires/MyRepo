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
fi

if ! test -f "$pubKeyFile"
then
    echo "Failed creating $pubKeyFile!"
    exit
fi

echo "Creating AWS resources and instance... Please wait."

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


# Parse logs to get routing table id, 
input=".tmp"
found=0
while IFS= read -r line
do
    if [ $found == 1 ]; then
        break
    fi
    if [[ $line =~ "[Create VPC subnet route table]" ]]; then
        found=1
    fi
done < "$input"

# get Route ID
delimiter="\"route_table_id\": \""
string=$line$delimiter
myarray=()
while [[ $string ]]; do
    myarray+=( "${string%%"$delimiter"*}" )
    string=${string#*"$delimiter"}
done
readarray -d"\"" -t strarr <<< "${myarray[1]}"
routeTableId=${strarr[0]}
echo "ROUTE TABLE ID: $routeTableId"

# Get VPC ID
delimiter="\"vpc_id\": \""
string=$line$delimiter
myarray=()
while [[ $string ]]; do
    myarray+=( "${string%%"$delimiter"*}" )
    string=${string#*"$delimiter"}
done
readarray -d"\"" -t strarr <<< "${myarray[1]}"
vpcId=${strarr[0]}
echo "VPC ID: $vpcId"

input=".tmp"
found=0
while IFS= read -r line
do
    if [ $found == 1 ]; then
        break
    fi
    if [[ $line =~ "Create EC2 instance" ]]; then
        found=1
    fi
done < "$input"

# get INSTANCE ID
delimiter="\"instance_ids\": [\""
string=$line$delimiter
myarray=()
while [[ $string ]]; do
    myarray+=( "${string%%"$delimiter"*}" )
    string=${string#*"$delimiter"}
done
readarray -d"\"" -t strarr <<< "${myarray[1]}"
instanceID=${strarr[0]}
echo "INSTANCE ID: $instanceID"

# get public IP
delimiter="\"public_ip\": \""
string=$line$delimiter
myarray=()
while [[ $string ]]; do
    myarray+=( "${string%%"$delimiter"*}" )
    string=${string#*"$delimiter"}
done
readarray -d"\"" -t strarr <<< "${myarray[1]}"
ipAdd=${strarr[0]}
echo "PUBLIC IP: $ipAdd"

# save details to .resources
echo $vpcId $instanceID $routeTableId $ipAdd >& .resources

# Connect to newly created instance and run commands in commands.sh
fileLen=${#myvar}-4
privateKey=${pubKeyFile:0:$fileLen}

cp -rf commands.sh.orig commands.sh
sed -i 's/_INSTANCE_ID_/'$instanceID'/' commands.sh

echo "PRIVATE KEY:  $privateKey"
chmod 400 $privateKey
ssh -i $privateKey  ubuntu@$ipAdd < commands.sh

echo -e "Webserver running. Check http://$ipAdd"

elif [ $1 == "delete" ]
then
    echo "Deleting AWS resources... Please wait."
    vpcId=$(cut -d " " -f 1 .resources)
    instanceId=$(cut -d " " -f 2 .resources)
    routeTableId=$(cut -d " " -f 3 .resources)
    ansible-playbook -v delete_ec2_resources.yml --extra-vars "vpc_id=$vpcId instance_id=$instanceId rt_id=$routeTableId" >& .tmp
    result=$(cat .tmp | grep "failed=0")
    if [ "${#result}" -eq 0 ]
    then
        echo -e "One of the Ansible tasks failed in deleting resources. "
        cat .tmp
    exit
fi

    echo "Deleted resources."
else
    echo "Invalid input"
    echo "Usage: ./deploy.sh create|delete"
    exit
fi


