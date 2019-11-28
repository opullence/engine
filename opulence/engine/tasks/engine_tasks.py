import inspect

from dynaconf import settings

import opulence.facts as all_facts
from opulence.common.celery.utils import sync_call

from ..factory import factory
from ..models.collector import Collector
from ..models.fact import Fact
from ..models.result import Result

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
    return Collector.objects().to_json()


@app.task(name="engine:load_facts")
def load_facts(flush=False):
    Fact.objects.delete()

    for m in inspect.getmembers(all_facts, inspect.isclass):
        Fact(**m[1]().get_info()).save()


@app.task(name="engine:get_facts")
def get_facts():
    return Fact.objects().to_json()


@app.task(name="engine:execute_collector")
def execute_collector(collector_name, fact):
    print("===================")
    for f in Fact.objects():
        if f.plugin_data["name"] == fact["input_type"]:
            fact_cls = getattr(all_facts, f.plugin_data["name"])
            fact_inst = fact_cls(**fact["fields"])
            result = sync_call(
                collectors_app,
                "collectors:execute_collector_by_name",
                100,
                args=[collector_name, fact_inst],
            )
            result_json = result.to_json()
            print("!!!!!!!!!!!!!!!!!!")
            print(result_json)
            print("!!!!!!!!!!!!!")
            print(result_json["collector_data"])
            Result(
                collector_data=result_json["collector_data"],
                clock=result_json["clock"],
                input=result_json["input"],
                output=result_json["output"],
                identifier=result_json["identifier"],
                status=result_json["status"],
            ).save()

            return result_json
    return "Nope"


@app.task(name="engine:get_results")
def get_results():
    return Result.objects().to_json()
