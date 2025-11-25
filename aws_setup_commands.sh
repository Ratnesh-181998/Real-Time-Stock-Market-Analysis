#!/bin/bash

# AWS Setup Script (Simulated)
# This script lists the AWS CLI commands to set up the infrastructure.
# You must have 'aws-cli' installed and configured ('aws configure').

KEY_NAME="kafka-key-pair"
SG_NAME="kafka-sg"
INSTANCE_TYPE="t2.medium"
AMI_ID="ami-0c55b159cbfafe1f0" # Amazon Linux 2 (US-East-2), change for your region!
BUCKET_NAME="stock-analysis-data-$(date +%s)"

echo "--- Starting AWS Setup ---"

# 1. Create Key Pair
echo "Creating Key Pair..."
aws ec2 create-key-pair --key-name $KEY_NAME --query 'KeyMaterial' --output text > $KEY_NAME.pem
chmod 400 $KEY_NAME.pem

# 2. Create Security Group
echo "Creating Security Group..."
SG_ID=$(aws ec2 create-security-group --group-name $SG_NAME --description "Kafka Security Group" --output text)
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 9092 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 2181 --cidr 0.0.0.0/0

# 3. Launch EC2 Instance
echo "Launching EC2 Instance ($INSTANCE_TYPE)..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-group-ids $SG_ID \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "Waiting for instance $INSTANCE_ID to be running..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
echo "Instance Running at IP: $PUBLIC_IP"

# 4. Create S3 Bucket
echo "Creating S3 Bucket: $BUCKET_NAME"
aws s3 mb s3://$BUCKET_NAME

echo "--- Setup Complete ---"
echo "SSH into your instance:"
echo "ssh -i $KEY_NAME.pem ec2-user@$PUBLIC_IP"
echo ""
echo "Then install Kafka using the commands in AWS_DEPLOYMENT.md"
