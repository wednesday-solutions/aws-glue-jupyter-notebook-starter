#!/bin/bash

# Original file
GLUE_FILE="assets/output.yaml"

# Iterate through the job directories
for JOB_DIR in src/jobs/*; do
  echo "Processing directory: $JOB_DIR"
  JOB_NAME_RAW=$(basename $JOB_DIR)
  JOB_NAME="$(tr '[:lower:]' '[:upper:]' <<< ${JOB_NAME_RAW:0:1})${JOB_NAME_RAW:1}" # Capitalizing the first letter
  echo "Job Name: $JOB_NAME"
  
  # Read the .env file line by line
  YAML_PATH=".Resources.Glue${JOB_NAME}.Properties.DefaultArguments"
  while IFS="=" read -r key value || [ -n "$key" ]; do
    # Skip comments and empty lines
    [[ $key =~ ^# ]] && continue
    [[ -z $key ]] && continue
    echo "Key: $key, Value: $value"

    # Define the yq command to append the key and value to the YAML file
    STYLE="style=\"double\""

    yq_command="yq e '$YAML_PATH.\"--$key\" = \"$value\"' -i $GLUE_FILE"
    eval $yq_command
  done < "$JOB_DIR/.env"
  # yq $YAML_PATH.' ... style="double" |= .' $GLUE_FILE
done