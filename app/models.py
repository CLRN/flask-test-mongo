from mongoengine import Document
from mongoengine import StringField, ReferenceField, ListField, FileField, IntField


class Security(Document):
    object_id = StringField(required=True)
    ticker = StringField()

    def __unicode__(self):
        return self.object_id

    def __repr__(self):
        return self.object_id


class Analysis(Document):
    name = StringField(required=True)
    input = FileField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name


class Tick(Document):
    sequence = IntField(required=True)
    analysis = ReferenceField(Analysis, required=True)
    pdump = StringField()
    bpipe = StringField()
    security = ReferenceField(Security, required=True)

    def __repr__(self):
        return str(self.sequence) + str(self.analysis)
