help: ## Show this help message
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

compile: ## Compile the GSP.proto file to generate Python code
	protoc --python_out=./output GSP.proto
	protoc --pyi_out=./output GSP.proto