from django.conf import settings


def google_analytics(request):
    return {'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY}


def uservoice(request):
    return {'USERVOICE_WIDGET': settings.USERVOICE_WIDGET}
