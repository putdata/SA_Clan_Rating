from django import template

from ..models import WebUser

register = template.Library()

@register.simple_tag
def user_set(user_id):
    user = WebUser.objects.filter(user_id=user_id)[0]
    return user


@register.simple_tag
def get_user_name(user_id):
    user = WebUser.objects.filter(user_id=user_id)[0]
    return user.name


@register.simple_tag
def get_DH_time(time):
    return time.strftime('%m-%d %H:%M')