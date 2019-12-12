from ..factory import factory, mongoClient

from .models import Scan

from opulence.common.utils import generate_uuid
from opulence.engine.facts import services as facts_services
import opulence.engine.collectors.tasks as collectors_tasks
import opulence.engine.collectors.signatures as remote_ctrl


app = factory.engine_app


@app.task(base=mongoClient.CacheMongoClient, name="engine:scan.get")
def get(external_identifier=None):
    with get.db as connection:
        if external_identifier is not None:
            return Scan.objects(external_identifier=external_identifier).get().to_json()
        return Scan.objects().to_json()


@app.task(base=mongoClient.CacheMongoClient, name="engine:scan.flush")
def flush():
    with flush.db as connection:
        Scan.objects.delete()


@app.task(name="engine:scan.quick")
def quick_scan(collector_name, facts):
    external_id = str(generate_uuid())


    f = facts_services.fact_from_json(facts)
    store_result = app.signature("engine:scan.__store_result", args=[external_id])
    c = remote_ctrl.launch(collector_name, f) | store_result
    c.apply_async()
    return external_id


# @app.task(name="engine:execute_collector")
# def execute_collector(collector_name, fact):
#     for f in Fact.objects():
#         if f.plugin_data["name"] == fact["input_type"]:
#             splitted_path = f.plugin_data["canonical_name"].split(".")
#             module = import_module(".".join(splitted_path[:-1]))
#             fact_cls = getattr(module, splitted_path[-1])
#             fact_inst = fact_cls(**fact["fields"])
#             result = sync_call(
#                 collectors_app,
#                 "collectors:execute_collector_by_name",
#                 100,
#                 args=[collector_name, fact_inst],
#             )
#             result_json = result.to_json()
#             Result(
#                 collector_data=result_json["collector_data"],
#                 clock=result_json["clock"],
#                 input=result_json["input"],
#                 output=result_json["output"],
#                 identifier=result_json["identifier"],
#                 status=result_json["status"],
#             ).save()

#             return result_json
#     return "Nope"


@app.task(base=mongoClient.CacheMongoClient, name="engine:scan.__store_result")
def __store_result(result, eid):
    scan_data = result.get_info()
    with __store_result.db as connection:
        Scan(external_identifier=eid, results=[scan_data]).save()
 