from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.settings import DB_PATH


def get_reading_db_url():
    # ------------- SQLITE -------------
    # url = 'sqlite:///teste.db'
    url = URL.create(
        drivername="sqlite",
        database=DB_PATH
    )

    # ------------- POSTGRESQL -------------
    # url = f"postgresql+psycopg2://{DatabaseEnv.DB_USER}:{DatabaseEnv.DB_PASSWORD}@{DatabaseEnv.DB_HOST}:{DatabaseEnv.DB_PORT}/{DatabaseEnv.DB_NAME}"
    # url = URL.create(drivername="postgresql+psycopg2",
    #            username=DatabaseEnv.DB_USER,
    #            password=DatabaseEnv.DB_PASSWORD,
    #            host=DatabaseEnv.DB_HOST,
    #            port=DatabaseEnv.DB_PORT,
    #            database=DatabaseEnv.DB_NAME)

    # ------------- MYSQL -------------
    # url = f"mysql+mysqlconnector://{DatabaseEnv.DB_USER}:{DatabaseEnv.DB_PASSWORD}@{DatabaseEnv.DB_HOST}:{DatabaseEnv.DB_PORT}/{DatabaseEnv.DB_NAME}"
    # url = URL.create(drivername="mysql+mysqlconnector",
    #            username=DatabaseEnv.DB_USER,
    #            password=DatabaseEnv.DB_PASSWORD,
    #            host=DatabaseEnv.DB_HOST,
    #            port=DatabaseEnv.DB_PORT,
    #            database=DatabaseEnv.DB_NAME)

    return url.render_as_string(hide_password=False)

def get_writing_db_url():
    # ------------- SQLITE -------------
    # url = 'sqlite:///teste.db'
    url = URL.create(
        drivername="sqlite",
        database=DB_PATH
    )

    # ------------- POSTGRESQL -------------
    # url = f"postgresql+psycopg2://{DatabaseEnv.DB_USER}:{DatabaseEnv.DB_PASSWORD}@{DatabaseEnv.DB_HOST}:{DatabaseEnv.DB_PORT}/{DatabaseEnv.DB_NAME}"
    # url = URL.create(drivername="postgresql+psycopg2",
    #            username=DatabaseEnv.DB_USER,
    #            password=DatabaseEnv.DB_PASSWORD,
    #            host=DatabaseEnv.DB_HOST,
    #            port=DatabaseEnv.DB_PORT,
    #            database=DatabaseEnv.DB_NAME)


    # ------------- MYSQL -------------
    # url = f"mysql+mysqlconnector://{DatabaseEnv.DB_USER}:{DatabaseEnv.DB_PASSWORD}@{DatabaseEnv.DB_HOST}:{DatabaseEnv.DB_PORT}/{DatabaseEnv.DB_NAME}"
    # url = URL.create(drivername="mysql+mysqlconnector",
    #            username=DatabaseEnv.DB_USER,
    #            password=DatabaseEnv.DB_PASSWORD,
    #            host=DatabaseEnv.DB_HOST,
    #            port=DatabaseEnv.DB_PORT,
    #            database=DatabaseEnv.DB_NAME)

    return url.render_as_string(hide_password=False)

reading_engine = create_engine(get_reading_db_url(), echo=False)
writing_engine = create_engine(get_writing_db_url(), echo=False)

ReadingSession = sessionmaker(
    bind=reading_engine,
    class_=Session,
    autoflush=True,  # Takes updated object data from database
    autocommit=False,
    expire_on_commit=True,  # Remove object instance info
    info=None,
)

WritingSession = sessionmaker(
    bind=writing_engine,
    class_=Session,
    autoflush=True,  # Takes updated object data from database
    autocommit=False,
    expire_on_commit=True,  # Remove object instance info
    info=None,
)
