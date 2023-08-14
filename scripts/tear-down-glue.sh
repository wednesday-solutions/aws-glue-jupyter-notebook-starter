#!/bin/sh -e

export "REGION=$(yq e '.region' config/properties.yml)"
export "STACK_NAME=$(yq e '.stack_name' config/properties.yml)"

echo "aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION"
aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION