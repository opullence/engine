import inspect
from importlib import import_module

from opulence.engine.factory import mongoClient
from .models import Fact


def fact_from_json(json_obj):
    with mongoClient.mongo_client():
        for f in Fact.objects():
            if f.external_identifier == json_obj["input_type"]:
                splitted_path = f.plugin_data["canonical_name"].split(".")
                module = import_module(".".join(splitted_path[:-1]))
                fact_cls = getattr(module, splitted_path[-1])
                return fact_cls(**json_obj["fields"])
    return None