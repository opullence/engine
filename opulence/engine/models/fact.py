import mongoengine


class Fact(mongoengine.DynamicDocument):
    meta = {"strict": False}
