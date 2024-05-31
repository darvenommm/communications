from django import template
from django.urls import reverse_lazy

register = template.Library()


@register.inclusion_tag("calls/tags/include_header.html", name="include_header")
def include_header(current_path: str, is_auth: bool):
    links_for_all = [
        {
            "url": reverse_lazy("home"),
            "text": "Home",
        },
    ]

    links_for_auth = [
        {
            "url": reverse_lazy("choosing_operators"),
            "text": "Choosing operators",
        },
        {
            "url": reverse_lazy("calls_history"),
            "text": "Call history",
        },
    ]

    return {
        "links_for_all": links_for_all,
        "links_for_auth": links_for_auth,
        "current_path": current_path,
        "is_auth": is_auth,
    }
