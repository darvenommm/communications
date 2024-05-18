from django.urls import path

from .views import SubscribersView, CallRoomView


app_name = "calls"

urlpatterns = [
    path("subscribers/", SubscribersView.as_view(), name="subscribers"),
    path("call-room/<uuid:call_room_id>", CallRoomView.as_view(), name="call_room"),
]
