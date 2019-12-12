from dynaconf import settings
from mongoengine import connect

from opulence.common.configuration import configure_celery
from opulence.common.patterns import Singleton


class Factory(Singleton):
    def __init__(self):
        self.engine_app = None
        self.remote_collectors = None

    def setup(self, **kwargs):
        self.engine_app = configure_celery(settings.REDIS, **kwargs)

        self.remote_collectors = configure_celery(
            settings.REMOTE_COLLECTOR.redis, **kwargs
        )

    @staticmethod
    def mongo_client():
        mongodb_config = settings.MONGO
        return connect(
            mongodb_config["database"],
            host=mongodb_config["url"],
            serverSelectionTimeoutMS=mongodb_config["connect_timeout"]
        )
