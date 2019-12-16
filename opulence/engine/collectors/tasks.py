import opulence.engine.collectors.signatures as collectors_s
from opulence.engine.collectors.models import Collector

from ..factory import factory, mongoClient

app = factory.engine_app


@app.task(base=mongoClient.CacheMongoClient, name="engine:collectors.get")
def get():
    with get.db as connection:
        return Collector.objects().to_json()


@app.task(name="engine:collectors.load")
def load():
    store_result = app.signature("engine:__store_collectors")

    chain = collectors_s.load() | collectors_s.list() | store_result
    chain.apply_async()


@app.task(base=mongoClient.CacheMongoClient, name="engine:collectors.flush")
def flush():
    with flush.db as connection:
        Collector.objects.delete()


@app.task(base=mongoClient.CacheMongoClient, name="engine:collectors.info")
def info(external_identifier):
    with info.db as connection:
        return (
            Collector.objects(external_identifier=external_identifier).first().to_json()
        )


@app.task(name="engine:collectors.launch")
def launch(collector_name, fact):
    return collectors_s.launch(collector_name, fact).apply_async()


@app.task(base=mongoClient.CacheMongoClient, name="engine:__store_collectors")
def __store_collectors(collectors):
    with __store_collectors.db as connection:
        for collector_data in collectors:
            if not Collector.objects(
                external_identifier=collector_data["plugin_data"]["name"]
            ):  # TODO: upsert
                Collector(
                    external_identifier=collector_data["plugin_data"]["name"],
                    **collector_data
                ).save()


# https://docs.celeryproject.org/en/latest/userguide/canvas.html
# http://docs.celeryproject.org/en/latest/userguide/tasks.html?highlight=state#states
