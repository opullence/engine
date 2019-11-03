import mongoengine

from .plugin import Plugin


class Collector(mongoengine.Document):
    active_scanning = mongoengine.BooleanField()

    allowed_input = mongoengine.ListField(
        mongoengine.ListField(mongoengine.StringField())
    )

    plugin_data = mongoengine.EmbeddedDocumentField(Plugin)
