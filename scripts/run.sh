docker build -t aws-glue-notebook-starter .

JUPYTER_WORKSPACE_LOCATION=$(pwd)
PROFILE_NAME=default

docker run -it -v ~/.aws:/home/glue_user/.aws -v $JUPYTER_WORKSPACE_LOCATION:/home/glue_user/workspace/jupyter_workspace/ -e ENVIRONMENT_NAME=local -e AWS_PROFILE=$PROFILE_NAME -e DISABLE_SSL=true --rm -p 4040:4040 -p 18080:18080 -p 8998:8998 -p 8888:8888 --name glue_jupyter_lab aws-glue-notebook-starter /home/glue_user/jupyter/jupyter_start.sh