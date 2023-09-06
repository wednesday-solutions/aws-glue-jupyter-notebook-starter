#!/bin/bash 

python3 -m pip install wheel
python3 setup.py bdist_wheel

export "BUCKET_NAME=$(yq e '.bucket_name' config/properties.yml)"
for JOB_DIR in ./src/jobs/job*; do
  JOB_NAME_RAW=$(basename $JOB_DIR)
  JOB_NAME="$(tr '[:lower:]' '[:upper:]' <<< ${JOB_NAME_RAW:0:1})${JOB_NAME_RAW:1}" # Capitalizing the first letter
  YAML_PATH=".Resources.Glue${JOB_NAME}.Properties.DefaultArguments"
  key="--additional-python-modules"
  value="s3://$BUCKET_NAME/lib/$1"
  yq_command="yq e '$YAML_PATH.\"$key\" = \"$value\"' -i assets/output.yaml"
  eval $yq_command
done