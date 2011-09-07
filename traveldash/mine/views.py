
from django.http import Http404
from django.template.response import TemplateResponse

from traveldash.mine.models import Dashboard

def dashboard(request, dashboard_slug):
    try:
        dashboard = Dashboard.objects.get(user=request.user, slug=dashboard_slug)
    except Dashboard.DoesNotExist:
        raise Http404
    
    return TemplateResponse(request, "mine/dashboard.html", {'dashboard': dashboard})
