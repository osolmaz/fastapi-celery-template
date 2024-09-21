###################
# Postgres config #
###################

DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_celery_boilerplate"
)
CELERY_BROKER_URL = "sqla+" + DATABASE_URL
CELERY_RESULT_BACKEND = "db+" + DATABASE_URL
CONNECT_ARGS = {}

#################
# SQLite config #
#################

# TEST_DATABASE_PATH = "./testdb.sqlite"

# # We use the same database for the broker and the result backend for now
# CELERY_DATABASE_PATH = TEST_DATABASE_PATH

# # Celery configuration
# CELERY_BROKER_URL = "sqla+sqlite:///" + CELERY_DATABASE_PATH
# CELERY_RESULT_BACKEND = "db+sqlite:///" + CELERY_DATABASE_PATH
# DATABASE_URL = "sqlite:///" + TEST_DATABASE_PATH
# CONNECT_ARGS = {"check_same_thread": False}