# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Deleting field 'DashboardRoute.from_stop_code'
        db.delete_column('mine_dashboardroute', 'from_stop_code')

        # Deleting field 'DashboardRoute.to_stop_code'
        db.delete_column('mine_dashboardroute', 'to_stop_code')

        # Adding field 'DashboardRoute.from_stop_ref'
        db.add_column('mine_dashboardroute', 'from_stop_ref', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

        # Adding field 'DashboardRoute.to_stop_ref'
        db.add_column('mine_dashboardroute', 'to_stop_ref', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

        for dr in orm.DashboardRoute.objects.all():
            dr.from_stop_ref = "%s:%s" % (dr.from_stop.source_id, dr.from_stop.stop_id)
            dr.to_stop_ref = "%s:%s" % (dr.to_stop.source_id, dr.to_stop.stop_id)
            dr.save()

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'DashboardRoute.from_stop_code'
        raise RuntimeError("Cannot reverse this migration. 'DashboardRoute.from_stop_code' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'DashboardRoute.to_stop_code'
        raise RuntimeError("Cannot reverse this migration. 'DashboardRoute.to_stop_code' and its values cannot be restored.")

        # Deleting field 'DashboardRoute.from_stop_ref'
        db.delete_column('mine_dashboardroute', 'from_stop_ref')

        # Deleting field 'DashboardRoute.to_stop_ref'
        db.delete_column('mine_dashboardroute', 'to_stop_ref')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 15, 18, 33, 18, 800991)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 2, 15, 18, 33, 18, 800785)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gtfs.agency': {
            'Meta': {'unique_together': "(('source', 'agency_id'),)", 'object_name': 'Agency'},
            'agency_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mine.GTFSSource']", 'null': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'gtfs.block': {
            'Meta': {'unique_together': "(('source', 'block_id'),)", 'object_name': 'Block'},
            'block_id': ('django.db.models.fields.TextField', [], {'max_length': '20', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mine.GTFSSource']", 'null': 'True'})
        },
        'gtfs.calendar': {
            'Meta': {'object_name': 'Calendar'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'friday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gtfs.Service']", 'unique': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'sunday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wednesday': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'gtfs.calendardate': {
            'Meta': {'object_name': 'CalendarDate'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'exception_type': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'calendar_exceptions'", 'to': "orm['gtfs.Service']"})
        },
        'gtfs.fare': {
            'Meta': {'unique_together': "(('source', 'fare_id'),)", 'object_name': 'Fare'},
            'currency_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'fare_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_method': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mine.GTFSSource']", 'null': 'True'}),
            'transfer_duration': ('django.db.models.fields.IntegerField', [], {}),
            'transfers': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'gtfs.farerule': {
            'Meta': {'object_name': 'FareRule'},
            'contains': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fare_rule_contains'", 'null': 'True', 'to': "orm['gtfs.Zone']"}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fare_rule_destinations'", 'null': 'True', 'to': "orm['gtfs.Zone']"}),
            'fare': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rules'", 'to': "orm['gtfs.Fare']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fare_rule_origins'", 'null': 'True', 'to': "orm['gtfs.Zone']"}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fare_rules'", 'null': 'True', 'to': "orm['gtfs.Route']"})
        },
        'gtfs.frequency': {
            'Meta': {'object_name': 'Frequency'},
            'end_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'end_time_days': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'headway_secs': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'start_time_days': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'frequencies'", 'to': "orm['gtfs.Trip']"})
        },
        'gtfs.route': {
            'Meta': {'unique_together': "(('agency', 'route_id'),)", 'object_name': 'Route'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'routes'", 'null': 'True', 'to': "orm['gtfs.Agency']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.TextField', [], {}),
            'route_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'route_type': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'text_color': ('django.db.models.fields.TextField', [], {'max_length': '6', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000', 'blank': 'True'})
        },
        'gtfs.service': {
            'Meta': {'unique_together': "(('source', 'service_id'),)", 'object_name': 'Service'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_id': ('django.db.models.fields.TextField', [], {'max_length': '20', 'db_index': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mine.GTFSSource']", 'null': 'True'})
        },
        'gtfs.shape': {
            'Meta': {'unique_together': "(('source', 'shape_id'),)", 'object_name': 'Shape'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.contrib.gis.db.models.fields.LineStringField', [], {'null': 'True'}),
            'shape_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mine.GTFSSource']", 'null': 'True'})
        },
        'gtfs.stop': {
            'Meta': {'unique_together': "(('source', 'stop_id'),)", 'object_name': 'Stop'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'location_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'parent_station': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_stops'", 'null': 'True', 'to': "orm['gtfs.Stop']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mine.GTFSSource']", 'null': 'True'}),
            'stop_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stops'", 'null': 'True', 'to': "orm['gtfs.Zone']"})
        },
        'gtfs.stoptime': {
            'Meta': {'ordering': "('trip', 'stop_sequence')", 'object_name': 'StopTime'},
            'arrival_days': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'arrival_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'departure_days': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'departure_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'drop_off_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pickup_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'shape_dist_travelled': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'times'", 'to': "orm['gtfs.Stop']"}),
            'stop_headsign': ('django.db.models.fields.TextField', [], {}),
            'stop_sequence': ('django.db.models.fields.IntegerField', [], {}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stop_times'", 'to': "orm['gtfs.Trip']"})
        },
        'gtfs.transfer': {
            'Meta': {'object_name': 'Transfer'},
            'from_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transfers_from'", 'to': "orm['gtfs.Stop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_transfer_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'to_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transfers_to'", 'to': "orm['gtfs.Stop']"}),
            'transfer_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'gtfs.trip': {
            'Meta': {'unique_together': "(('service', 'trip_id'), ('route', 'trip_id'))", 'object_name': 'Trip'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trips'", 'null': 'True', 'to': "orm['gtfs.Block']"}),
            'direction_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'headsign': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trips'", 'to': "orm['gtfs.Route']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trips'", 'to': "orm['gtfs.Service']"}),
            'shape': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trips'", 'null': 'True', 'to': "orm['gtfs.Shape']"}),
            'short_name': ('django.db.models.fields.TextField', [], {}),
            'trip_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'gtfs.universalcalendar': {
            'Meta': {'unique_together': "(('service', 'date'),)", 'object_name': 'UniversalCalendar'},
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'all_dates'", 'to': "orm['gtfs.Service']"})
        },
        'gtfs.zone': {
            'Meta': {'unique_together': "(('source', 'zone_id'),)", 'object_name': 'Zone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mine.GTFSSource']", 'null': 'True'}),
            'zone_id': ('django.db.models.fields.TextField', [], {'max_length': '20', 'db_index': 'True'})
        },
        'mine.alert': {
            'Meta': {'object_name': 'Alert'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alerts'", 'to': "orm['mine.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'valid_from': ('django.db.models.fields.DateField', [], {}),
            'valid_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'mine.city': {
            'Meta': {'object_name': 'City'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_center': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'map_zoom': ('django.db.models.fields.PositiveIntegerField', [], {'default': '11'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mine.dashboard': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'Dashboard'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dashboards'", 'to': "orm['mine.City']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_viewed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dashboards'", 'to': "orm['auth.User']"}),
            'warning_time': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'})
        },
        'mine.dashboardroute': {
            'Meta': {'object_name': 'DashboardRoute'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'routes'", 'to': "orm['mine.Dashboard']"}),
            'from_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dashboard_routes_start'", 'null': 'True', 'to': "orm['gtfs.Stop']"}),
            'from_stop_ref': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'routes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gtfs.Route']", 'symmetrical': 'False'}),
            'to_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dashboard_routes_end'", 'null': 'True', 'to': "orm['gtfs.Stop']"}),
            'to_stop_ref': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'walk_time_end': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'walk_time_start': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'mine.gtfssource': {
            'Meta': {'object_name': 'GTFSSource'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sources'", 'to': "orm['mine.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'page_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'page_xpath': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'update_freq': ('django.db.models.fields.IntegerField', [], {'default': '14'}),
            'web_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'zip_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['gtfs', 'mine']
