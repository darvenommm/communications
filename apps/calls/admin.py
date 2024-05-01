from django.contrib import admin

from .models import Operator, Subscriber, SubscriberCall, OperatorSubscriber
from .admin_models import (
    OperatorAdmin,
    SubscriberAdmin,
    SubscriberCallAdmin,
    OperatorSubscriberAdmin,
)


models_for_registration = (
    (Operator, OperatorAdmin),
    (Subscriber, SubscriberAdmin),
    (SubscriberCall, SubscriberCallAdmin),
    (OperatorSubscriber, OperatorSubscriberAdmin),
)


for model, admin_model in models_for_registration:
    admin.register(model)(admin_model)
