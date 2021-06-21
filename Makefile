style:
	flake8 .

types:
	DJANGO_CONFIGURATION=Dev mypy --no-error-summary --allow-redefinition review_bot

check:
	make -j4 style types
