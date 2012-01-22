import urllib

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def help_tweet_url(context, dashboard):
    dashboard_url = context['request'].build_absolute_uri(dashboard.get_absolute_url())
    params = {
        'text': "help! my dashboard is broken!",
        'url': dashboard_url,
        'screen_name': "TravelDash",
    }
    url = "http://twitter.com/intent/tweet?" + urllib.urlencode(params)
    return url
