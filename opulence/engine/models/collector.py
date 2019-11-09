import mongoengine


class Collector(mongoengine.DynamicDocument):
    meta = {"strict": False}

    active_scanning = mongoengine.BooleanField()

    # allowed_input = mongoengine.ListField(
    #     mongoengine.StringField()
    # )

    # plugin_data = mongoengine.EmbeddedDocumentField(Plugin)
