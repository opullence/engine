import mongoengine


class Scan(mongoengine.DynamicDocument):
    meta = {"strict": False}

    external_identifier = mongoengine.StringField(primary_key=True)