from mongoengine import connect
from dynaconf import settings


from opulence.common.configuration import configure_celery
from opulence.common.patterns import Singleton


class Factory(Singleton):
    def __init__(self):
        self.mongoDB = None
        self.engine_app = None
        self.remote_collectors = None

    def setup(self, **kwargs):
        self.engine_app = configure_celery(
            settings.REDIS, **kwargs
        )

        self.remote_collectors = configure_celery(
            settings.REMOTE_COLLECTOR.redis, **kwargs
        )
        self.setup_mongodb()

    def setup_mongodb(self):
        mongodb_config = settings.MONGO
        # try:
        self.mongoDB = connect(
            mongodb_config["database"],
            host=mongodb_config["url"],
            serverSelectionTimeoutMS=mongodb_config["connect_timeout"],
        )
        self.mongoDB.server_info()
        # except Exception as err:
        #     print("MongoDB connect error:", err)
