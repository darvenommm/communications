from django.contrib import admin

from calls.models import Operator, Subscriber, SubscriberCall
from calls.admin_models import OperatorAdmin, SubscriberAdmin, SubscriberCallAdmin


admin.site.register(Operator, OperatorAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(SubscriberCall, SubscriberCallAdmin)
