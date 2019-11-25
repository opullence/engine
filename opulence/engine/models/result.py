import mongoengine


class Result(mongoengine.DynamicDocument):
    meta = {"strict": False}
