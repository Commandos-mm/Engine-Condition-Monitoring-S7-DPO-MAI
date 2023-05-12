.PHONY: install
install:
	pip install poetry
	poetry install

.PHONY: run-local
run-local:
	poetry run streamlit run src/main.py

.PHONY: build
build: 
	docker build . 
