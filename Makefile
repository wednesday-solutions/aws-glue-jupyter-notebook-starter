create-glue-job:
	@echo "running create-glue-job"

create-s3-bucket:
	@echo "running create-s3-bucket"

create-iam-role:
	@echo "running create-iam-role"

setup: create-iam-role create-s3-bucket create-glue-job
	@echo "Setup done..."
