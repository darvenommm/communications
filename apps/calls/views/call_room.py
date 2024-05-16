from django.views.generic import TemplateView


class CallRoomView(TemplateView):
    template_name = "calls/pages/call_room.html"
