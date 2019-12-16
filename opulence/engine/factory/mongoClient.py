from celery import Task
from dynaconf import settings
from mongoengine import connect


def mongo_client():
    mongodb_config = settings.MONGO
    return connect(
        mongodb_config["database"],
        host=mongodb_config["url"],
        serverSelectionTimeoutMS=mongodb_config["connect_timeout"],
    )


class CacheMongoClient(Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = mongo_client()
        return self._db
