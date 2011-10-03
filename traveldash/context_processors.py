from django.conf import settings

def google_analytics(request):
    return {'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY}
