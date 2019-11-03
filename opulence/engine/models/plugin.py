import mongoengine


class Plugin(mongoengine.EmbeddedDocument):
    name = mongoengine.StringField(required=True, unique=True)
    version = mongoengine.StringField()
    author = mongoengine.StringField()
    category = mongoengine.StringField()
    description = mongoengine.StringField()
    status = mongoengine.IntField()
    error = mongoengine.StringField()
    canonical_name = mongoengine.StringField()
