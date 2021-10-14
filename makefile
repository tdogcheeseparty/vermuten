test:
	python -m unittest discover tests "*_tests.py"

run:
	VERMUTEN_CONFIG=demo.json && gunicorn app:app

win-run:
	set VERMUTEN_CONFIG=demo.json && waitress-serve --listen="127.0.0.1:8000" app:app
