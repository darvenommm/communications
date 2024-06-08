"""Register calls admins model."""

from django.contrib import admin

from .admin_models import OperatorAdmin, SubscriberCallAdmin
from .models import Operator, SubscriberCall

models_for_registration = ((Operator, OperatorAdmin), (SubscriberCall, SubscriberCallAdmin))


for model, admin_model in models_for_registration:
    admin.register(model)(admin_model)
