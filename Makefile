help: ## Show this help message
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

clean_output: ## Remove all generated output files
	rm -f ./src/examples/output/*

validate_json: ## Validate all .gsp.json files against the gsp.schema.json
	python scripts/validate_gsp_schema.py

###############################################################################

pytest: ## Run pytest on the tests/ directory
	PYTHONPATH=${PWD} cd tests && pytest -W ignore::DeprecationWarning


pytest_verbose: ## Run pytest in verbose mode on the tests/ directory
	cd tests && pytest -v -W ignore::DeprecationWarning


##############################################################################

lint: lint_src lint_examples ## Run pyright type checker on src and examples

lint_src: ## Run pyright type checker on ./src
	pyright src/

lint_examples: ## Run pyright type checker on ./examples
	pyright examples/

##########################################################################

network_server_dev: ## Run the network server in development mode
	watchmedo auto-restart -d ./src -d ./scripts -p="*.py" -R  -- python ./scripts/network_server.py

network_server: ## Run the network server
	python ./scripts/network_server.py

##############################################################################

run_all_examples: ## Run all examples to check they run without error
	python scripts/run_all_examples.py

check_expected_output: ## Check that the output files match the expected output files
	python scripts/check_expected_output.py

test: lint pytest_verbose run_all_examples check_expected_output ## Run all tests
	@echo "All tests passed!"