# #!/bin/sh

PROJECT_NAME="$1"
STACK_NAME="$PROJECT_NAME-cf-stack"
REGION="$2"
FILE_PATH="./data/raw/sample.csv"
LANDING_PATH="source/"
BUCKET_NAME="$PROJECT_NAME-bucket"

jinja2 assets/glue-template.yaml.j2 --format=json -D prefix=$PROJECT_NAME > assets/output.yaml

aws cloudformation create-stack \
  --stack-name $STACK_NAME \
  --template-body file://assets/output.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --region $2 > /dev/null

# Wait for the Stack to be Created
aws cloudformation wait stack-create-complete \
  --stack-name $STACK_NAME \
  --region $REGION

if [ $? -eq 0 ]; then
  echo "Stack creation complete."

  # Copy the CSV file to S3
  aws s3 cp $FILE_PATH s3://$BUCKET_NAME/$LANDING_PATH

  if [ $? -eq 0 ]; then
    echo "CSV file uploaded successfully."
  else
    echo "CSV file upload failed."
  fi
else
  echo "Stack creation failed."
fi


./scripts/convert-notebooks-to-scripts.sh


for JOB_DIR in ./src/jobs/job*; do
  JOB_NAME=$(basename $JOB_DIR) # Extract job name from folder (e.g., job1, job2)

  # Define the destination path in S3
  DESTINATION="s3://$BUCKET_NAME/scripts/$JOB_NAME/"

  # Upload the script.py file to the destination path
  aws s3 cp "$JOB_DIR/script.py" "$DESTINATION"

  # Check if the upload was successful
  if [ $? -eq 0 ]; then
    echo "Uploaded $JOB_NAME/script.py successfully."
  else
    echo "Failed to upload $JOB_NAME/script.py."
  fi
  echo "\nBUCKET_NAME=$BUCKET_NAME" >> $JOB_DIR/.env
  echo "\nSOURCE_CRAWLER=${PROJECT_NAME}SourceCrawler" >> $JOB_DIR/.env
done

yq_command="yq e '.bucket_name="\"$BUCKET_NAME\""' -i config/properties.yml"
eval $yq_command
yq_command="yq e '.region="\"$REGION\""' -i config/properties.yml"
eval $yq_command
yq_command="yq e '.stack_name="\"$STACK_NAME\""' -i config/properties.yml"
eval $yq_command

aws glue start-crawler --name $PROJECT_NAME"SourceCrawler" --region $REGION