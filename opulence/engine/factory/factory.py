from mongoengine import connect

from opulence.common.configuration import configure_celery, get_conf
from opulence.common.patterns import Singleton


class Factory(Singleton):
    def __init__(self):
        self.mongoDB = None
        self.engine_app = None
        self.remote_collectors = None
        self.config = get_conf()

    def setup(self, **kwargs):
        self.engine_app = configure_celery(
            self.config["engine"]["databases"]["queue_database"], **kwargs
        )

        self.remote_collectors = configure_celery(
            self.config["remote_collectors"]["queue_database"], **kwargs
        )
        self.setup_mongodb()

    def setup_mongodb(self):
        mongodb_config = self.config["engine"]["databases"]["mongoDB"]
        # try:
        self.mongoDB = connect(
            mongodb_config["database"],
            host=mongodb_config["url"],
            serverSelectionTimeoutMS=mongodb_config["connect_timeout"],
        )
        self.mongoDB.server_info()
        # except Exception as err:
        #     print("MongoDB connect error:", err)
