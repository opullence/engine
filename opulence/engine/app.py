from .scans import tasks
from .factory import factory
from .facts import tasks as fact_tasks
from .collectors import tasks as collectors_tasks

from celery.signals import celeryd_init

app = factory.engine_app

#Load things on startup
@celeryd_init.connect
def startup(sender=None, conf=None, **kwargs):
    fact_tasks.flush.delay()
    fact_tasks.load.delay()

    collectors_tasks.flush.delay()
    collectors_tasks.load.delay()    