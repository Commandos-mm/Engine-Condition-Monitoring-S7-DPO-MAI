.PHONY: install
install:
	pip install poetry
	poetry install

.PHONY: run-local
run-local:
	poetry run streamlit run src/main.py 2> /dev/null

.PHONY: build
build: 
	docker build . 
