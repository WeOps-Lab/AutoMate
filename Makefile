.PHONY: debug run help build start push
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

debug: ## 以Debug模式运行
	python ./main.py


run-worker:
	 celery -A server.workers worker --loglevel=info

# 以Prod模式运行
run:
	uvicorn main:bootstrap.application --host 0.0.0.0 --port 8000 --workers 5 --access-log --use-colors


build:
	rm -Rf ./oracle-instantclient-basic-21.8.0.0.0-1.x86_64.rpm &&\
	wget https://www.abc.net/videos/oracle-instantclient-basic-21.8.0.0.0-1.x86_64.rpm &&\
	docker build -t auto-mate .
