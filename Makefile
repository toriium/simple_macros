revision:
	poetry run alembic -c src/data/db_orm/alembic.ini revision --autogenerate

upgrade:
	poetry run alembic -c src/data/db_orm/alembic.ini upgrade head