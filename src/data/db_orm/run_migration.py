import time

from alembic import command
from alembic.config import Config

from src.data.db_orm.connection import get_writing_db_url
from src.settings import BASE_DIR


def run_migration() -> None:
    for _ in range(5):
        time.sleep(1)
        try:
            path = f"{BASE_DIR}/src/data/db_orm/alembic"
            alembic_cfg = Config()
            alembic_cfg.set_main_option("script_location", path)
            alembic_cfg.set_main_option("sqlalchemy.url", get_writing_db_url())
            command.upgrade(alembic_cfg, "head")
            break
        except Exception as e:
            print(e)
    else:
        raise RuntimeError("Could not run migration")
