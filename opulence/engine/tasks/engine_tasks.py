from opulence.common.celery.utils import sync_call
from opulence.common.configuration import get_conf

from ..factory import factory
from ..models.collector import Collector

app = factory.engine_app
collectors_app = factory.remote_collectors
timeout = get_conf()["engine"]["celery_request_timeout"]


@app.task(name="engine:load_collectors")
def load_collectors(flush=False):
    if flush:
        Collector.objects.delete()
    sync_call(collectors_app, "collectors:reload_collectors", timeout, args=[True])
    collectors = sync_call(
        collectors_app, "collectors:list_collectors", timeout, args=[]
    )
    for collector_name in collectors:
        collector_data = sync_call(
            collectors_app, "collectors:collector_info", timeout, args=[collector_name]
        )
        Collector(**collector_data).save()


@app.task(name="engine:get_collectors")
def get_collectors():
    return Collector.objects().to_json()  # do this in the serializer instead
