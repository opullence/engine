from celery.signals import celeryd_init

from . import tasks
from .factory import factory

app = factory.engine_app

# Run some tasks on startup
@celeryd_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    tasks.engine_tasks.load_collectors(flush=True)
