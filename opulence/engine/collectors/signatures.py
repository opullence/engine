from opulence.common.celery.utils import async_call

from ..factory import factory

collectors_app = factory.remote_collectors


def load():
    return collectors_app.signature("collectors:reload_collectors", immutable=True)

def list():
    return collectors_app.signature("collectors:list_collectors", immutable=True)

def info():
    pass

def launch(collector_name, input_fact):
    return collectors_app.signature("collectors:execute_collector_by_name", args=[collector_name, input_fact])
