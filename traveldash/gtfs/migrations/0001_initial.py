# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Source'
        db.create_table('gtfs_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('gtfs', ['Source'])

        # Adding model 'Agency'
        db.create_table('gtfs_agency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Source'], null=True)),
            ('agency_id', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('gtfs', ['Agency'])

        # Adding unique constraint on 'Agency', fields ['source', 'agency_id']
        db.create_unique('gtfs_agency', ['source_id', 'agency_id'])

        # Adding model 'Stop'
        db.create_table('gtfs_stop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Source'], null=True)),
            ('stop_id', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'], null=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('is_station', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parent_station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Stop'], null=True)),
        ))
        db.send_create_signal('gtfs', ['Stop'])

        # Adding unique constraint on 'Stop', fields ['source', 'stop_id']
        db.create_unique('gtfs_stop', ['source_id', 'stop_id'])

        # Adding model 'RouteType'
        db.create_table('gtfs_routetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gtfs', ['RouteType'])

        # Adding model 'Route'
        db.create_table('gtfs_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route_id', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Agency'])),
            ('short_name', self.gf('django.db.models.fields.TextField')()),
            ('long_name', self.gf('django.db.models.fields.TextField')()),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('route_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.RouteType'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1000)),
            ('colour', self.gf('django.db.models.fields.TextField')()),
            ('text_colour', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gtfs', ['Route'])

        # Adding unique constraint on 'Route', fields ['agency', 'route_id']
        db.create_unique('gtfs_route', ['agency_id', 'route_id'])

        # Adding model 'Block'
        db.create_table('gtfs_block', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Source'], null=True)),
            ('block_id', self.gf('django.db.models.fields.TextField')(max_length=20, db_index=True)),
        ))
        db.send_create_signal('gtfs', ['Block'])

        # Adding unique constraint on 'Block', fields ['source', 'block_id']
        db.create_unique('gtfs_block', ['source_id', 'block_id'])

        # Adding model 'Trip'
        db.create_table('gtfs_trip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip_id', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Route'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Service'])),
            ('headsign', self.gf('django.db.models.fields.TextField')()),
            ('short_name', self.gf('django.db.models.fields.TextField')()),
            ('inbound', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('outbound', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Block'], null=True)),
            ('shape', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Shape'], null=True)),
        ))
        db.send_create_signal('gtfs', ['Trip'])

        # Adding unique constraint on 'Trip', fields ['service', 'trip_id']
        db.create_unique('gtfs_trip', ['service_id', 'trip_id'])

        # Adding unique constraint on 'Trip', fields ['route', 'trip_id']
        db.create_unique('gtfs_trip', ['route_id', 'trip_id'])

        # Adding model 'Arrangements'
        db.create_table('gtfs_arrangements', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gtfs', ['Arrangements'])

        # Adding model 'StopTime'
        db.create_table('gtfs_stoptime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Trip'])),
            ('arrival_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('arrival_days', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('departure_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('departure_days', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Stop'])),
            ('stop_sequence', self.gf('django.db.models.fields.IntegerField')()),
            ('stop_headsign', self.gf('django.db.models.fields.TextField')()),
            ('pickup_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pickup', null=True, to=orm['gtfs.Arrangements'])),
            ('drop_off_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dropoff', null=True, to=orm['gtfs.Arrangements'])),
            ('shape_dist_travelled', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('gtfs', ['StopTime'])

        # Adding model 'Service'
        db.create_table('gtfs_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Source'], null=True)),
            ('service_id', self.gf('django.db.models.fields.TextField')(max_length=20, db_index=True)),
        ))
        db.send_create_signal('gtfs', ['Service'])

        # Adding unique constraint on 'Service', fields ['source', 'service_id']
        db.create_unique('gtfs_service', ['source_id', 'service_id'])

        # Adding model 'Calendar'
        db.create_table('gtfs_calendar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gtfs.Service'], unique=True)),
            ('monday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tuesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wednesday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thursday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('friday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('saturday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sunday', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('gtfs', ['Calendar'])

        # Adding model 'CalendarDate'
        db.create_table('gtfs_calendardate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Service'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('add_or_remove_service', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('gtfs', ['CalendarDate'])

        # Adding model 'PaymentMethod'
        db.create_table('gtfs_paymentmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gtfs', ['PaymentMethod'])

        # Adding model 'TransferPermission'
        db.create_table('gtfs_transferpermission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('limited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ntransfers', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('gtfs', ['TransferPermission'])

        # Adding model 'FareRule'
        db.create_table('gtfs_farerule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Agency'])),
            ('farerule_id', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('currency_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('payment_method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.PaymentMethod'])),
            ('transfer_permission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.TransferPermission'])),
            ('transfer_duration', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('gtfs', ['FareRule'])

        # Adding model 'Zone'
        db.create_table('gtfs_zone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone_id', self.gf('django.db.models.fields.TextField')(max_length=20, db_index=True)),
        ))
        db.send_create_signal('gtfs', ['Zone'])

        # Adding model 'RouteFareRules'
        db.create_table('gtfs_routefarerules', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Route'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['RouteFareRules'])

        # Adding model 'OriginFareRules'
        db.create_table('gtfs_originfarerules', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['OriginFareRules'])

        # Adding model 'DestinationFareRules'
        db.create_table('gtfs_destinationfarerules', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['DestinationFareRules'])

        # Adding model 'ContainsFareRules'
        db.create_table('gtfs_containsfarerules', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['ContainsFareRules'])

        # Adding model 'Shape'
        db.create_table('gtfs_shape', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Source'], null=True)),
            ('shape_id', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('line_string', self.gf('django.contrib.gis.db.models.fields.LineStringField')(null=True)),
        ))
        db.send_create_signal('gtfs', ['Shape'])

        # Adding model 'Frequency'
        db.create_table('gtfs_frequency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Trip'])),
            ('start_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('start_time_days', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('end_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('end_time_days', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('headway_secs', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('gtfs', ['Frequency'])

        # Adding model 'TransferType'
        db.create_table('gtfs_transfertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gtfs', ['TransferType'])

        # Adding model 'Transfers'
        db.create_table('gtfs_transfers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transfer_from_stop', to=orm['gtfs.Stop'])),
            ('to_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transfer_to_stop', to=orm['gtfs.Stop'])),
            ('transfer_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.TransferType'])),
            ('min_transfer_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('gtfs', ['Transfers'])

    def backwards(self, orm):

        # Removing unique constraint on 'Service', fields ['source', 'service_id']
        db.delete_unique('gtfs_service', ['source_id', 'service_id'])

        # Removing unique constraint on 'Trip', fields ['route', 'trip_id']
        db.delete_unique('gtfs_trip', ['route_id', 'trip_id'])

        # Removing unique constraint on 'Trip', fields ['service', 'trip_id']
        db.delete_unique('gtfs_trip', ['service_id', 'trip_id'])

        # Removing unique constraint on 'Block', fields ['source', 'block_id']
        db.delete_unique('gtfs_block', ['source_id', 'block_id'])

        # Removing unique constraint on 'Route', fields ['agency', 'route_id']
        db.delete_unique('gtfs_route', ['agency_id', 'route_id'])

        # Removing unique constraint on 'Stop', fields ['source', 'stop_id']
        db.delete_unique('gtfs_stop', ['source_id', 'stop_id'])

        # Removing unique constraint on 'Agency', fields ['source', 'agency_id']
        db.delete_unique('gtfs_agency', ['source_id', 'agency_id'])

        # Deleting model 'Source'
        db.delete_table('gtfs_source')

        # Deleting model 'Agency'
        db.delete_table('gtfs_agency')

        # Deleting model 'Stop'
        db.delete_table('gtfs_stop')

        # Deleting model 'RouteType'
        db.delete_table('gtfs_routetype')

        # Deleting model 'Route'
        db.delete_table('gtfs_route')

        # Deleting model 'Block'
        db.delete_table('gtfs_block')

        # Deleting model 'Trip'
        db.delete_table('gtfs_trip')

        # Deleting model 'Arrangements'
        db.delete_table('gtfs_arrangements')

        # Deleting model 'StopTime'
        db.delete_table('gtfs_stoptime')

        # Deleting model 'Service'
        db.delete_table('gtfs_service')

        # Deleting model 'Calendar'
        db.delete_table('gtfs_calendar')

        # Deleting model 'CalendarDate'
        db.delete_table('gtfs_calendardate')

        # Deleting model 'PaymentMethod'
        db.delete_table('gtfs_paymentmethod')

        # Deleting model 'TransferPermission'
        db.delete_table('gtfs_transferpermission')

        # Deleting model 'FareRule'
        db.delete_table('gtfs_farerule')

        # Deleting model 'Zone'
        db.delete_table('gtfs_zone')

        # Deleting model 'RouteFareRules'
        db.delete_table('gtfs_routefarerules')

        # Deleting model 'OriginFareRules'
        db.delete_table('gtfs_originfarerules')

        # Deleting model 'DestinationFareRules'
        db.delete_table('gtfs_destinationfarerules')

        # Deleting model 'ContainsFareRules'
        db.delete_table('gtfs_containsfarerules')

        # Deleting model 'Shape'
        db.delete_table('gtfs_shape')

        # Deleting model 'Frequency'
        db.delete_table('gtfs_frequency')

        # Deleting model 'TransferType'
        db.delete_table('gtfs_transfertype')

        # Deleting model 'Transfers'
        db.delete_table('gtfs_transfers')

    models = {
        'gtfs.agency': {
            'Meta': {'unique_together': "(('source', 'agency_id'),)", 'object_name': 'Agency'},
            'agency_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Source']", 'null': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'gtfs.arrangements': {
            'Meta': {'object_name': 'Arrangements'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'gtfs.block': {
            'Meta': {'unique_together': "(('source', 'block_id'),)", 'object_name': 'Block'},
            'block_id': ('django.db.models.fields.TextField', [], {'max_length': '20', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Source']", 'null': 'True'})
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
            'add_or_remove_service': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Service']"})
        },
        'gtfs.containsfarerules': {
            'Meta': {'object_name': 'ContainsFareRules'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.FareRule']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Zone']"})
        },
        'gtfs.destinationfarerules': {
            'Meta': {'object_name': 'DestinationFareRules'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.FareRule']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Zone']"})
        },
        'gtfs.farerule': {
            'Meta': {'object_name': 'FareRule'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Agency']"}),
            'currency_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'farerule_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.PaymentMethod']"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'transfer_duration': ('django.db.models.fields.IntegerField', [], {}),
            'transfer_permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.TransferPermission']"})
        },
        'gtfs.frequency': {
            'Meta': {'object_name': 'Frequency'},
            'end_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'end_time_days': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'headway_secs': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'start_time_days': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Trip']"})
        },
        'gtfs.originfarerules': {
            'Meta': {'object_name': 'OriginFareRules'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.FareRule']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Zone']"})
        },
        'gtfs.paymentmethod': {
            'Meta': {'object_name': 'PaymentMethod'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'gtfs.route': {
            'Meta': {'unique_together': "(('agency', 'route_id'),)", 'object_name': 'Route'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Agency']"}),
            'colour': ('django.db.models.fields.TextField', [], {}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.TextField', [], {}),
            'route_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'route_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.RouteType']"}),
            'short_name': ('django.db.models.fields.TextField', [], {}),
            'text_colour': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1000'})
        },
        'gtfs.routefarerules': {
            'Meta': {'object_name': 'RouteFareRules'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Route']"}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.FareRule']"})
        },
        'gtfs.routetype': {
            'Meta': {'object_name': 'RouteType'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'gtfs.service': {
            'Meta': {'unique_together': "(('source', 'service_id'),)", 'object_name': 'Service'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_id': ('django.db.models.fields.TextField', [], {'max_length': '20', 'db_index': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Source']", 'null': 'True'})
        },
        'gtfs.shape': {
            'Meta': {'object_name': 'Shape'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_string': ('django.contrib.gis.db.models.fields.LineStringField', [], {'null': 'True'}),
            'shape_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Source']", 'null': 'True'})
        },
        'gtfs.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'gtfs.stop': {
            'Meta': {'unique_together': "(('source', 'stop_id'),)", 'object_name': 'Stop'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_station': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'parent_station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Stop']", 'null': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Source']", 'null': 'True'}),
            'stop_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Zone']", 'null': 'True'})
        },
        'gtfs.stoptime': {
            'Meta': {'object_name': 'StopTime'},
            'arrival_days': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'arrival_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'departure_days': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'departure_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'drop_off_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dropoff'", 'null': 'True', 'to': "orm['gtfs.Arrangements']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pickup_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pickup'", 'null': 'True', 'to': "orm['gtfs.Arrangements']"}),
            'shape_dist_travelled': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Stop']"}),
            'stop_headsign': ('django.db.models.fields.TextField', [], {}),
            'stop_sequence': ('django.db.models.fields.IntegerField', [], {}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Trip']"})
        },
        'gtfs.transferpermission': {
            'Meta': {'object_name': 'TransferPermission'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ntransfers': ('django.db.models.fields.IntegerField', [], {})
        },
        'gtfs.transfers': {
            'Meta': {'object_name': 'Transfers'},
            'from_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transfer_from_stop'", 'to': "orm['gtfs.Stop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_transfer_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'to_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transfer_to_stop'", 'to': "orm['gtfs.Stop']"}),
            'transfer_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.TransferType']"})
        },
        'gtfs.transfertype': {
            'Meta': {'object_name': 'TransferType'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'gtfs.trip': {
            'Meta': {'unique_together': "(('service', 'trip_id'), ('route', 'trip_id'))", 'object_name': 'Trip'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Block']", 'null': 'True'}),
            'headsign': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'outbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Route']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Service']"}),
            'shape': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Shape']", 'null': 'True'}),
            'short_name': ('django.db.models.fields.TextField', [], {}),
            'trip_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'gtfs.zone': {
            'Meta': {'object_name': 'Zone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone_id': ('django.db.models.fields.TextField', [], {'max_length': '20', 'db_index': 'True'})
        }
    }

    complete_apps = ['gtfs']
