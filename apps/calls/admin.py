from django.contrib import admin

from .models import Operator, SubscriberCall
from .admin_models import OperatorAdmin, SubscriberCallAdmin


models_for_registration = ((Operator, OperatorAdmin), (SubscriberCall, SubscriberCallAdmin))


for model, admin_model in models_for_registration:
    admin.register(model)(admin_model)
