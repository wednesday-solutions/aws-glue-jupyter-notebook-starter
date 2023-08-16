#!/bin/sh -x

STACK_NAME=$1
REGION=$2

# Function to create a change set
create_change_set() {
  aws cloudformation create-change-set \
    --stack-name $STACK_NAME \
    --template-body file://assets/output.yaml \
    --region $REGION \
    --capabilities CAPABILITY_NAMED_IAM \
    --change-set-name $STACK_NAME-change-set >> /dev/null
}

# Function to execute a change set
execute_change_set() {
  aws cloudformation execute-change-set \
    --stack-name $STACK_NAME \
    --change-set-name $STACK_NAME-change-set \
    --region $REGION  >> /dev/null
}

delete_change_set() {
  aws cloudformation delete-change-set \
    --stack-name $STACK_NAME \
    --change-set-name $STACK_NAME-change-set \
    --region $REGION  >> /dev/null
}
 
describe_check_and_execute () {
  # Check if the change set already exists
  change_set=$(aws cloudformation describe-change-set \
    --stack-name $STACK_NAME \
    --change-set-name $STACK_NAME-change-set \
    --region $REGION \
    --query 'StatusReason')

  echo $change_set


  no_new_info=$(echo $change_set | grep "Submit different information to create a change set")

  mismatch=$(echo $change_set | grep "mismatch with existing attribute Template")

  echo "no_new_info:"$no_new_info
  echo "mismatch:"$mismatch

  if [ -n "$no_new_info" ]; then
    echo "No new information in change set. Deleting it."
    delete_change_set
    exit 0

  elif [ -n "$mismatch" ]; then
    echo "Mismatch in change set. Deleting it"
    delete_change_set
  elif [ -n "$change_set" ]; then
    echo "Change set already exists. Executing it."
    execute_change_set
    exit 0
  fi
}



describe_check_and_execute

create_change_set

sleep 10

describe_check_and_execute