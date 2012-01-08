import json

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django import forms
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse
from django.conf import settings

from bootstrap.forms import BootstrapModelForm

from traveldash.mine.models import Dashboard, DashboardRoute
from traveldash.gtfs.models import Route, Stop


@vary_on_cookie
def home(request):
    example_dashboard = Dashboard.objects.order_by('?')[0]
    return TemplateResponse(request, "mine/home.html", {'example_dashboard': example_dashboard})

def login(request):
    return TemplateResponse(request, "login.html")

@vary_on_cookie
def dashboard(request, pk):
    try:
        dashboard = Dashboard.objects.get(pk=pk)
    except Dashboard.DoesNotExist:
        raise Http404

    return TemplateResponse(request, "mine/dashboard.html", {'dashboard': dashboard})

@vary_on_cookie
@cache_control(must_revalidate=True)
def dashboard_update(request, pk):
    try:
        dashboard = Dashboard.objects.get(pk=pk)
    except Dashboard.DoesNotExist:
        return HttpResponse(json.dumps({"error": "dashboard-not-found"}), status=404, content_type="application/json")

    content = dashboard.as_json()
    return HttpResponse(json.dumps(content), content_type="application/json")

@login_required
def dashboard_list(request):
    c = {
        'dashboard_list': Dashboard.objects.filter(user=request.user),
        'base_url': request.build_absolute_uri('/')[:-1],
    }
    return TemplateResponse(request, "mine/dashboard_list.html", c)


class RouteForm(BootstrapModelForm):
    class Meta:
        model = DashboardRoute
        fields = ('id', 'from_stop', 'walk_time_start', 'to_stop', 'walk_time_end',)
        widgets = {
            'from_stop': forms.TextInput(attrs={'class': 'gtfsStop'}),
            'to_stop': forms.TextInput(attrs={'class': 'gtfsStop'}),
        }

    def clean(self):
        cd = self.cleaned_data
        if ('from_stop' in cd) and ('to_stop' in cd):
            if not Route.objects.between_stops(cd['from_stop'], cd['to_stop']).count():
                raise forms.ValidationError("No Transport routes between the stops you've selected")
        return cd

    def stop_json(self):
        return json.dumps({
            'from_stop': self._stop_info(self['from_stop'].value()),
            'to_stop': self._stop_info(self['to_stop'].value()),
        })

    def _stop_info(self, stop_id):
        try:
            stop = Stop.objects.get(pk=stop_id)
            return {'id': stop.pk, 'name': stop.name, 'location': stop.location.tuple}
        except Stop.DoesNotExist:
            return None

RouteFormSet = inlineformset_factory(Dashboard, DashboardRoute, form=RouteForm, extra=1)


class DashboardForm(BootstrapModelForm):
    class Meta:
        model = Dashboard
        exclude = ('user',)


@login_required
def dashboard_create(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        if form.is_valid():
            dashboard = form.save(commit=False)
            dashboard.user = request.user
            route_formset = RouteFormSet(request.POST, instance=dashboard)
            if route_formset.is_valid():
                dashboard.save()
                route_formset.save()
                messages.success(request, "Created!")
                return HttpResponseRedirect(dashboard.get_absolute_url())
        else:
            route_formset = RouteFormSet(instance=Dashboard())
    else:
        form = DashboardForm()
        route_formset = RouteFormSet(instance=Dashboard())
    return TemplateResponse(request, "mine/dashboard_form.html", {'form': form, 'route_formset': route_formset, 'title':'New Dashboard', 'stopFusionTableId': settings.GTFS_STOP_FUSION_TABLE_ID})

@login_required
def dashboard_edit(request, pk):
    try:
        dashboard = Dashboard.objects.filter(user=request.user).get(pk=pk)
    except Dashboard.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = DashboardForm(request.POST, instance=dashboard)
        if form.is_valid():
            form.save(commit=False)
            route_formset = RouteFormSet(request.POST, instance=dashboard)
            if route_formset.is_valid():
                dashboard.save()
                route_formset.save()

                if dashboard.routes.count() == 0:
                    dashboard.delete()
                    messages.success(request, "Deleted empty dashboard")
                    return HttpResponseRedirect(reverse('traveldash.mine.views.dashboard_list'))
                else:
                    messages.success(request, "Saved")
                    return HttpResponseRedirect(dashboard.get_absolute_url())
    else:
        form = DashboardForm(instance=dashboard)
        route_formset = RouteFormSet(instance=dashboard)
    return TemplateResponse(request, "mine/dashboard_form.html", {'form': form, 'route_formset': route_formset, 'title':'Edit Dashboard', 'dashboard': dashboard, 'stopFusionTableId': settings.GTFS_STOP_FUSION_TABLE_ID})

class DashboardDelete(DeleteView):
    context_object_name="dashboard"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashboardDelete, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Dashboard.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('traveldash.mine.views.dashboard_list')