from typing import Type

from django.db.models import Field
from django.db.models.expressions import Expression


# django 5 docs - https://docs.djangoproject.com/en/5.0/ref/models/fields/#generatedfield
class GeneratedFields:
    def __init__(self, expression: Expression, output_field: Field, db_persist: bool) -> None: ...


GeneratedFieldsType = Type[GeneratedFields]
