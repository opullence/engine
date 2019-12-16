import inspect

import opulence.facts as all_facts
from opulence.common.facts import BaseFact

from ..factory import factory, mongoClient
from .models import Fact

app = factory.engine_app


@app.task(base=mongoClient.CacheMongoClient, name="engine:facts.get")
def get():
    with get.db as connection:
        return Fact.objects().to_json()


@app.task(base=mongoClient.CacheMongoClient, name="engine:facts.load")
def load():
    with load.db as connection:
        for m in inspect.getmembers(all_facts, inspect.isclass):
            fact_inst = m[1]()
            if isinstance(fact_inst, BaseFact):
                fact_info = fact_inst.get_info()
                external_id = fact_info["plugin_data"]["name"]
                if not Fact.objects(external_identifier=external_id):  # TODO: upsert
                    Fact(external_identifier=external_id, **fact_info).save()


@app.task(base=mongoClient.CacheMongoClient, name="engine:facts.flush")
def flush():
    with flush.db as connection:
        Fact.objects.delete()


@app.task(base=mongoClient.CacheMongoClient, name="engine:facts.info")
def info(fact_name):
    with info.db as connection:
        return Fact.objects(plugin_data__name=fact_name).first().to_json()
