.PHONY: tests

tests:
	mypy modelhub
	pycodestyle modelhub
	pytest -n 4 --dist loadgroup tests_modelhub/unit tests_modelhub/functional tests_modelhub

tests-bigquery:
# Similar to `tests`, but tests that can run against multiple databases will be run against BigQuery instead
# of Postgres. Note that most of our test-suite is postgres-only. The postgres-only tests will still run
# against Postgres
	mypy modelhub
	pycodestyle modelhub
	pytest --bigquery -n 8 --dist loadgroup tests_modelhub

tests-athena:
# Similar to `tests`, but tests that can run against multiple databases will be run against Athena instead
# of Postgres. Note that a lot of tests are not yet supported for athena. The postgres-only tests will still
# against Postgres
	mypy modelhub
	pycodestyle modelhub
	pytest --athena -n 8 --dist loadgroup tests_modelhub



tests-all:
# Similar to `tests`, but tests that can run against multiple databases will be run against both BigQuery
# and Postgres. Note that most of our test-suite is postgres-only. The postgres-only tests will still only
# run against Postgres
	mypy modelhub
	pycodestyle modelhub
	pytest --all -n 8 --dist loadgroup tests_modelhub
