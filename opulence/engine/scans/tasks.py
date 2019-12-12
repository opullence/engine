from ..factory import factory, mongoClient

from .models import Scan

from opulence.common.utils import generate_uuid
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
def quick_scan(collector_name, fact):
    external_id = str(generate_uuid())
    store_result = app.signature("engine:scan.__store_result", args=[external_id])
    c = remote_ctrl.launch(collector_name, fact) | store_result
    c.apply_async()
    return external_id


@app.task(base=mongoClient.CacheMongoClient, name="engine:scan.__store_result")
def __store_result(result, eid):
    scan_data = result.get_info()
    with __store_result.db as connection:
        Scan(external_identifier=eid, results=[scan_data]).save()
 