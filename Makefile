install-tools:
	@echo "Checking and installing tools..."
	@./scripts/install-yq-jinja.sh

infra: install-tools
	@echo "running infra...  $(name) $(region)"
	./scripts/create-glue-job.sh $(name) $(region)

local: install-tools
	@echo "running local... "
	./scripts/run.sh

env-to-args: install-tools
	@echo "running env-to-args..."
	./scripts/env-to-args.sh

notebooks-to-scripts: install-tools
	@echo "notebooks-to-scripts ..."
	./scripts/convert-notebooks-to-scripts.sh

update-infra: install-tools
	@echo "updating infrastructure $(name) $(region)"
	./scripts/update-glue-job.sh $(name) $(region)

teardown-infra: install-tools
	@echo "running teardown infra ..."
	./scripts/tear-down-glue.sh