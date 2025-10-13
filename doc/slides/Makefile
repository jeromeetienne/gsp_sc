help: ## Show this help message
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

all: technical_debt alternative_path ## Generate all slides

technical_debt: ## Generate technical_debt.pdf from technical_debt.md
	npx @marp-team/marp-cli@latest  --theme marpit-custom.css technical_debt.md -o ./output/technical_debt.pdf

alternative_path: ## Generate alternative_path.pdf from alternative_path.md
	npx @marp-team/marp-cli@latest  --theme marpit-custom.css alternative_path.md -o ./output/alternative_path.pdf