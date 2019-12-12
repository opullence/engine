from celery import Task

from . import factory


class CacheMongoClient(Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = factory.mongo_client()
        return self._db
