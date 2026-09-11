.PHONY: install test verify doctor demo serve

install:
	python -m pip install -e .

test:
	python -m unittest discover -s tests -v

verify:
	python scripts/verify_100_agents.py
	python -m compileall -q al_mehdi tests

doctor:
	python -m al_mehdi doctor

demo:
	python -m al_mehdi demo prompt_injection

serve:
	python -m al_mehdi serve

