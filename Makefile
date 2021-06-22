style:
	flake8 .

types:
	DJANGO_CONFIGURATION=Dev mypy --no-error-summary --allow-redefinition review_bot

check:
	make -j4 style types


test:
	 DJANGO_CONFIGURATION=Dev pytest --cov=review_bot --no-cov-on-fail --cov-fail-under=55 review_bot
