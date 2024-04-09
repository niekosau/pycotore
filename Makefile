default: venv
# Variables
VENV           = .venv
VENV_PYTHON    = $(VENV)/bin/python
SYSTEM_PYTHON  = $(or $(shell which python3.9), $(shell which python3), $(shell which python))
PYTHON         = $(or $(wildcard $(VENV_PYTHON)), $(SYSTEM_PYTHON))
venv:
	poetry env use python3.9

dev:
	poetry add --group=dev flake8 tox pytest pytest-cov
	$(PYTHON) setup.py develop

cleanup:
	rm -rf build/ dist/ .venv/

flake8:
	$(PYTHON) -m flake8 reclass

pytest:
	$(PYTHON) -m pytest -s -v
