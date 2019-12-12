from dynaconf import settings

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
