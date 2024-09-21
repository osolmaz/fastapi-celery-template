TEST_DATABASE_PATH = "./testdb.sqlite"

# We use the same database for the broker and the result backend for now
CELERY_DATABASE_PATH = TEST_DATABASE_PATH

# Celery configuration
CELERY_BROKER_URL = "sqla+sqlite:///" + CELERY_DATABASE_PATH
CELERY_RESULT_BACKEND = "db+sqlite:///" + CELERY_DATABASE_PATH
DATABASE_URL = "sqlite:///" + TEST_DATABASE_PATH
