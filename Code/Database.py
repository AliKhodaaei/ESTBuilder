from peewee import *
import uuid

proxy = Proxy()


def export_db(est, db_name):
    db = SqliteDatabase('Databases/EST_' + db_name)  # :memory:
    proxy.initialize(db)
    db.drop_tables([Entity, Reference])
    db.create_tables([Entity, Reference])
    for ent in est:
        ent.save()
    print(f'EST_{db_name} database exported successfully\n')


class BaseModel(Model):
    class Meta:
        database = proxy


class Entity(BaseModel):
    uid = UUIDField(default=uuid.uuid4)
    kind = CharField(max_length=100, null=True, default='')
    name = CharField(max_length=100, null=True, default='')
    type = CharField(max_length=100, null=True, default='')
    value = CharField(max_length=100, null=True, default='')
    scope = CharField(max_length=100, null=True, default='')
    modifier = CharField(max_length=100, null=True, default='')
    return_type = CharField(max_length=100, null=True, default='')
    exception = CharField(max_length=100, null=True, default='')

    def __str__(self):
        return f"Entity(kind: {self.kind}, name: {self.name}, type: {self.type}, value: {self.value}, scope: {self.scope}, modifier: {self.modifier}, return_type: {self.return_type}, exception: {self.exception})"


class Reference(BaseModel):
    uid = UUIDField(default=uuid.uuid4)
    kind = CharField(max_length=100, null=True, default='')
    referredId = CharField(max_length=100, null=True, default='')
    referrerId = CharField(max_length=100, null=True, default='')

    def __str__(self):
        return f"Reference(kind: {self.kind}, referredId: {self.referredId}, referrerId: {self.referrerId})"
