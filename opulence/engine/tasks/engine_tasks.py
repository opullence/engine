from dynaconf import settings
import inspect

import opulence.facts as all_facts
from opulence.common.celery.utils import sync_call

from ..factory import factory
from ..models.collector import Collector
from ..models.fact import Fact

app = factory.engine_app
collectors_app = factory.remote_collectors
timeout = settings.CELERY_TIMEOUT


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
    return Collector.objects().to_json()  # TODO: do this in the serializer instead


@app.task(name="engine:load_facts")
def load_facts(flush=False):
    Fact.objects.delete()
    
    for m in inspect.getmembers(all_facts, inspect.isclass):
        Fact(**m[1]().get_info()).save()


@app.task(name="engine:get_facts")
def get_facts():
    return Fact.objects().to_json()  # TODO: do this in the serializer instead

@app.task(name="engine:execute_collector")
def execute_collector(collector_name, fact):

    for m in inspect.getmembers(all_facts, inspect.isclass):
        fact_name = m[1]().get_info()["plugin_data"]["name"]
        if fact_name == fact["input_type"]:
            f = m[1](**fact["fields"])
            return sync_call(
                collectors_app, "collectors:execute_collector_by_name", 1000, args=[collector_name, f]
            )
    return "NOPE"
