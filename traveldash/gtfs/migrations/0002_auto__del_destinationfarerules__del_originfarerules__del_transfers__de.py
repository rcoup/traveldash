# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'DestinationFareRules'
        db.delete_table('gtfs_destinationfarerules')

        # Deleting model 'OriginFareRules'
        db.delete_table('gtfs_originfarerules')

        # Deleting model 'Transfers'
        db.delete_table('gtfs_transfers')

        # Deleting model 'Arrangements'
        db.delete_table('gtfs_arrangements')

        # Deleting model 'RouteFareRules'
        db.delete_table('gtfs_routefarerules')

        # Deleting model 'ContainsFareRules'
        db.delete_table('gtfs_containsfarerules')

        # Adding model 'ContainsFareRule'
        db.create_table('gtfs_containsfarerule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['ContainsFareRule'])

        # Adding model 'RouteFareRule'
        db.create_table('gtfs_routefarerule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Route'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['RouteFareRule'])

        # Adding model 'Transfer'
        db.create_table('gtfs_transfer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transfer_from_stop', to=orm['gtfs.Stop'])),
            ('to_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transfer_to_stop', to=orm['gtfs.Stop'])),
            ('transfer_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.TransferType'])),
            ('min_transfer_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('gtfs', ['Transfer'])

        # Adding model 'OriginFareRule'
        db.create_table('gtfs_originfarerule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['OriginFareRule'])

        # Adding model 'DestinationFareRule'
        db.create_table('gtfs_destinationfarerule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['DestinationFareRule'])

        # Adding model 'Arrangement'
        db.create_table('gtfs_arrangement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gtfs', ['Arrangement'])

        # Changing field 'StopTime.pickup_type'
        db.alter_column('gtfs_stoptime', 'pickup_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['gtfs.Arrangement']))

        # Changing field 'StopTime.drop_off_type'
        db.alter_column('gtfs_stoptime', 'drop_off_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['gtfs.Arrangement']))


    def backwards(self, orm):
        
        # Adding model 'DestinationFareRules'
        db.create_table('gtfs_destinationfarerules', (
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['DestinationFareRules'])

        # Adding model 'OriginFareRules'
        db.create_table('gtfs_originfarerules', (
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['OriginFareRules'])

        # Adding model 'Transfers'
        db.create_table('gtfs_transfers', (
            ('from_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transfer_from_stop', to=orm['gtfs.Stop'])),
            ('to_stop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transfer_to_stop', to=orm['gtfs.Stop'])),
            ('transfer_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.TransferType'])),
            ('min_transfer_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('gtfs', ['Transfers'])

        # Adding model 'Arrangements'
        db.create_table('gtfs_arrangements', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gtfs', ['Arrangements'])

        # Adding model 'RouteFareRules'
        db.create_table('gtfs_routefarerules', (
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Route'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['RouteFareRules'])

        # Adding model 'ContainsFareRules'
        db.create_table('gtfs_containsfarerules', (
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['ContainsFareRules'])

        # Deleting model 'ContainsFareRule'
        db.delete_table('gtfs_containsfarerule')

        # Deleting model 'RouteFareRule'
        db.delete_table('gtfs_routefarerule')

        # Deleting model 'Transfer'
        db.delete_table('gtfs_transfer')

        # Deleting model 'OriginFareRule'
        db.delete_table('gtfs_originfarerule')

        # Deleting model 'DestinationFareRule'
        db.delete_table('gtfs_destinationfarerule')

        # Deleting model 'Arrangement'
        db.delete_table('gtfs_arrangement')

        # Changing field 'StopTime.pickup_type'
        db.alter_column('gtfs_stoptime', 'pickup_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['gtfs.Arrangements']))

        # Changing field 'StopTime.drop_off_type'
        db.alter_column('gtfs_stoptime', 'drop_off_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['gtfs.Arrangements']))


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
        'gtfs.arrangement': {
            'Meta': {'object_name': 'Arrangement'},
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
        'gtfs.containsfarerule': {
            'Meta': {'object_name': 'ContainsFareRule'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.FareRule']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Zone']"})
        },
        'gtfs.destinationfarerule': {
            'Meta': {'object_name': 'DestinationFareRule'},
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
        'gtfs.originfarerule': {
            'Meta': {'object_name': 'OriginFareRule'},
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
        'gtfs.routefarerule': {
            'Meta': {'object_name': 'RouteFareRule'},
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
            'drop_off_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dropoff'", 'null': 'True', 'to': "orm['gtfs.Arrangement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pickup_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pickup'", 'null': 'True', 'to': "orm['gtfs.Arrangement']"}),
            'shape_dist_travelled': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Stop']"}),
            'stop_headsign': ('django.db.models.fields.TextField', [], {}),
            'stop_sequence': ('django.db.models.fields.IntegerField', [], {}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Trip']"})
        },
        'gtfs.transfer': {
            'Meta': {'object_name': 'Transfer'},
            'from_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transfer_from_stop'", 'to': "orm['gtfs.Stop']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'min_transfer_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'to_stop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transfer_to_stop'", 'to': "orm['gtfs.Stop']"}),
            'transfer_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.TransferType']"})
        },
        'gtfs.transferpermission': {
            'Meta': {'object_name': 'TransferPermission'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ntransfers': ('django.db.models.fields.IntegerField', [], {})
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
