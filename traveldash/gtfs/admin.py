from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from traveldash.gtfs.models import *


class ReadOnlyAdminMixin(object):
    _rw_fields = ()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        from django.contrib.admin.options import modelform_factory, flatten_fieldsets, curry

        if not hasattr(self, "_readonly_fields"):
            if self.declared_fieldsets:
                fields = flatten_fieldsets(self.declared_fieldsets)
            else:
                fields = None
            if self.exclude is None:
                exclude = []
            else:
                exclude = list(self.exclude)
            exclude.extend(self.readonly_fields)

            # if exclude is an empty list we pass None to be consistant with the
            # default on modelform_factory
            exclude = exclude or None
            defaults = {
                "form": self.form,
                "fields": fields,
                "exclude": exclude,
                "formfield_callback": curry(self.formfield_for_dbfield, request=request),
            }
            self._readonly_fields = modelform_factory(self.model, **defaults).base_fields
        return self._readonly_fields.keys()


class ReadOnlyModelAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    pass


class ReadOnlyOSMGeoAdmin(ReadOnlyAdminMixin, OSMGeoAdmin):
    modifiable = False

    def get_readonly_fields(self, request, obj=None):
        from django.contrib.gis.forms import GeometryField
        if not hasattr(self, '_readonly_fields'):
            super(ReadOnlyOSMGeoAdmin, self).get_readonly_fields(request, obj)

            for field_name, field in self._readonly_fields.items():
                if isinstance(field, GeometryField):
                    if field_name not in self.readonly_fields:
                        del self._readonly_fields[field_name]

        return super(ReadOnlyOSMGeoAdmin, self).get_readonly_fields(request, obj)


class StopAdmin(ReadOnlyOSMGeoAdmin):
    search_fields = ('code', 'name', 'desc')

admin.site.register(Agency, ReadOnlyModelAdmin)
admin.site.register(Stop, StopAdmin)
admin.site.register(Route, ReadOnlyModelAdmin)
admin.site.register(Block, ReadOnlyModelAdmin)
admin.site.register(Trip, ReadOnlyModelAdmin)
admin.site.register(StopTime, ReadOnlyModelAdmin)
admin.site.register(Fare, ReadOnlyModelAdmin)
admin.site.register(FareRule, ReadOnlyModelAdmin)
admin.site.register(Zone, ReadOnlyModelAdmin)
admin.site.register(Shape, ReadOnlyOSMGeoAdmin)
admin.site.register(Frequency, ReadOnlyModelAdmin)
admin.site.register(Transfer, ReadOnlyModelAdmin)
admin.site.register(UniversalCalendar, ReadOnlyModelAdmin)

if settings.GTFS_SOURCE_MODEL == "gtfs.Source":
    admin.site.register(Source)
