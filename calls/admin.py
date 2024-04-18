from django.contrib import admin

from calls.models import Operator, Subscriber, SubscriberCall


admin.site.register(Operator)
admin.site.register(Subscriber)
admin.site.register(SubscriberCall)
