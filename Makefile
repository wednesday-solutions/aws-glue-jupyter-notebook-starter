infra:
	@echo "running infra...  $(name) $(region)"
	./scripts/create-glue-job.sh $(name) $(region)

local:
	@echo "running local... "
	./scripts/run.sh

env-to-args: 
	@echo "running env-to-args..."
	./scripts/env-to-args.sh

- notebooks-to-scripts: 
	@echo "- notebooks-to-scripts ..."
	./scripts/convert-notebooks-to-scripts.sh