from django.db import models


class ConcatString(models.Func):
    arg_joiner = " || "
    template = "%(expressions)s"
