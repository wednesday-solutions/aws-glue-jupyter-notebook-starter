#!/bin/sh 
STACK_NAME=$1
REGION=$2

aws cloudformation create-change-set \
  --stack-name $STACK_NAME \
  --template-body file://assets/output.yaml \
  --region $REGION \
  --capabilities CAPABILITY_NAMED_IAM \
  --change-set-name $STACK_NAME-change-set >> /dev/null

# Describe the change set to see if there are changes
changes=$(aws cloudformation describe-change-set \
  --stack-name $STACK_NAME \
  --change-set-name $STACK_NAME-change-set \
  --query 'StatusReason')

# If changes are present, execute the change set
if [ "$changes" != "\"The submitted information didn't contain changes. Submit different information to create a change set.\"" ]; then
  aws cloudformation execute-change-set \
    --stack-name $STACK_NAME \
    --change-set-name $STACK_NAME-change-set
else
  echo "No changes to apply"
fi