import json
from datetime import datetime

import opulence.engine.collectors.signatures as remote_ctrl
import opulence.engine.collectors.tasks as collectors_tasks
from opulence.common.job import StatusCode
from opulence.common.utils import generate_uuid, now
from opulence.engine.facts import services as facts_services

from ..factory import factory, mongoClient
from .models import Result, Scan, Stats

app = factory.engine_app


@app.task(base=mongoClient.CacheMongoClient, name="engine:scan.get")
def get(external_identifier):
    with get.db as connection:
        scan = json.loads(
            Scan.objects(external_identifier=external_identifier).get().to_json()
        )
        scan["results"] = json.loads(
            Result.objects(scan_identifier=external_identifier).to_json()
        )

        scan["stats"]["start_date"] = datetime.strptime(
            scan["stats"]["start_date"], "%Y,%m,%d,%H,%M,%S,%f"
        ).isoformat()
        if "end_date" in scan["stats"]:
            scan["stats"]["end_date"] = datetime.strptime(
                scan["stats"]["end_date"], "%Y,%m,%d,%H,%M,%S,%f"
            ).isoformat()
        return scan


@app.task(base=mongoClient.CacheMongoClient, name="engine:scan.list")
def list():
    with list.db as connection:
        return Scan.objects().to_json()


@app.task(base=mongoClient.CacheMongoClient, name="engine:scan.flush")
def flush():
    with flush.db as connection:
        Scan.objects.delete()


@app.task(base=mongoClient.CacheMongoClient, name="engine:scan.start_scan")
def start_scan(eid, scan_type="Unknown"):
    with start_scan.db as connection:
        Scan(
            external_identifier=eid,
            status=(StatusCode.started, ""),
            stats=Stats(),
            scan_type=scan_type,
        ).save()


@app.task(base=mongoClient.CacheMongoClient, name="engine:scan.stop_scan")
def stop_scan(eid):
    with stop_scan.db as connection:
        Scan(external_identifier=eid).update(
            set__status=(StatusCode.finished, ""), set__stats__end_date=now()
        )


@app.task(name="engine:scan.quick")
def quick_scan(collector_name, facts):
    external_id = str(generate_uuid())

    f = facts_services.fact_from_json(facts)
    start_scan = app.signature(
        "engine:scan.start_scan", args=[external_id, "Quick scan"]
    )
    new_result = app.signature("engine:scan.new_result", args=[external_id])
    stop_scan = app.signature(
        "engine:scan.stop_scan", args=[external_id], immutable=True
    )

    c = start_scan | remote_ctrl.launch(collector_name, f) | new_result | stop_scan
    c.apply_async()
    return external_id


@app.task(
    base=mongoClient.CacheMongoClient, name="engine:scan.new_result", ignore_result=True
)
def new_result(result, eid):
    scan_data = result.get_info()
    with new_result.db as connection:
        Scan(external_identifier=eid).update(inc__stats__number_of_results=1)
        Result(scan_identifier=eid, **scan_data).save()
