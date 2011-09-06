# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'PaymentMethod'
        db.delete_table('gtfs_paymentmethod')

        # Deleting model 'ContainsFareRule'
        db.delete_table('gtfs_containsfarerule')

        # Deleting model 'RouteFareRule'
        db.delete_table('gtfs_routefarerule')

        # Deleting model 'TransferType'
        db.delete_table('gtfs_transfertype')

        # Deleting model 'OriginFareRule'
        db.delete_table('gtfs_originfarerule')

        # Deleting model 'DestinationFareRule'
        db.delete_table('gtfs_destinationfarerule')

        # Deleting model 'RouteType'
        db.delete_table('gtfs_routetype')

        # Deleting model 'Arrangement'
        db.delete_table('gtfs_arrangement')

        # Deleting field 'FareRule.transfer_permission'
        db.delete_column('gtfs_farerule', 'transfer_permission_id')

        # Adding field 'FareRule.transfers'
        db.add_column('gtfs_farerule', 'transfers', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # Adding field 'FareRule.route'
        db.add_column('gtfs_farerule', 'route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Route'], null=True), keep_default=False)

        # Adding field 'FareRule.origin'
        db.add_column('gtfs_farerule', 'origin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fare_rule_origins', null=True, to=orm['gtfs.Zone']), keep_default=False)

        # Adding field 'FareRule.destination'
        db.add_column('gtfs_farerule', 'destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fare_rule_destinations', null=True, to=orm['gtfs.Zone']), keep_default=False)

        # Adding field 'FareRule.contains'
        db.add_column('gtfs_farerule', 'contains', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fare_rule_contains', null=True, to=orm['gtfs.Zone']), keep_default=False)

        # Renaming column for 'FareRule.payment_method' to match new field type.
        db.rename_column('gtfs_farerule', 'payment_method_id', 'payment_method')
        # Changing field 'FareRule.payment_method'
        db.alter_column('gtfs_farerule', 'payment_method', self.gf('django.db.models.fields.IntegerField')())

        # Removing index on 'FareRule', fields ['payment_method']
        db.delete_index('gtfs_farerule', ['payment_method_id'])

        # Renaming column for 'Transfer.transfer_type' to match new field type.
        db.rename_column('gtfs_transfer', 'transfer_type_id', 'transfer_type')
        # Changing field 'Transfer.transfer_type'
        db.alter_column('gtfs_transfer', 'transfer_type', self.gf('django.db.models.fields.IntegerField')())

        # Removing index on 'Transfer', fields ['transfer_type']
        db.delete_index('gtfs_transfer', ['transfer_type_id'])

        # Changing field 'Route.short_name'
        db.alter_column('gtfs_route', 'short_name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Adding index on 'Route', fields ['short_name']
        db.create_index('gtfs_route', ['short_name'])

        # Renaming column for 'Route.route_type' to match new field type.
        db.rename_column('gtfs_route', 'route_type_id', 'route_type')
        # Changing field 'Route.route_type'
        db.alter_column('gtfs_route', 'route_type', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Route.text_color'
        db.alter_column('gtfs_route', 'text_color', self.gf('django.db.models.fields.TextField')(max_length=6))

        # Changing field 'Route.color'
        db.alter_column('gtfs_route', 'color', self.gf('django.db.models.fields.CharField')(max_length=6))

        # Deleting field 'Stop.is_station'
        db.delete_column('gtfs_stop', 'is_station')

        # Adding field 'Stop.location_type'
        db.add_column('gtfs_stop', 'location_type', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Changing field 'Stop.code'
        db.alter_column('gtfs_stop', 'code', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Adding index on 'Stop', fields ['code']
        db.create_index('gtfs_stop', ['code'])

        # Renaming column for 'StopTime.pickup_type' to match new field type.
        db.rename_column('gtfs_stoptime', 'pickup_type_id', 'pickup_type')
        # Changing field 'StopTime.pickup_type'
        db.alter_column('gtfs_stoptime', 'pickup_type', self.gf('django.db.models.fields.IntegerField')())

        # Removing index on 'StopTime', fields ['pickup_type']
        db.delete_index('gtfs_stoptime', ['pickup_type_id'])

        # Renaming column for 'StopTime.drop_off_type' to match new field type.
        db.rename_column('gtfs_stoptime', 'drop_off_type_id', 'drop_off_type')
        # Changing field 'StopTime.drop_off_type'
        db.alter_column('gtfs_stoptime', 'drop_off_type', self.gf('django.db.models.fields.IntegerField')())

        # Removing index on 'StopTime', fields ['drop_off_type']
        db.delete_index('gtfs_stoptime', ['drop_off_type_id'])


    def backwards(self, orm):
        
        # Adding index on 'StopTime', fields ['drop_off_type']
        db.create_index('gtfs_stoptime', ['drop_off_type_id'])

        # Adding index on 'StopTime', fields ['pickup_type']
        db.create_index('gtfs_stoptime', ['pickup_type_id'])

        # Removing index on 'Stop', fields ['code']
        db.delete_index('gtfs_stop', ['code'])

        # Removing index on 'Route', fields ['short_name']
        db.delete_index('gtfs_route', ['short_name'])

        # Adding index on 'Transfer', fields ['transfer_type']
        db.create_index('gtfs_transfer', ['transfer_type_id'])

        # Adding index on 'FareRule', fields ['payment_method']
        db.create_index('gtfs_farerule', ['payment_method_id'])

        # Adding model 'PaymentMethod'
        db.create_table('gtfs_paymentmethod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gtfs', ['PaymentMethod'])

        # Adding model 'ContainsFareRule'
        db.create_table('gtfs_containsfarerule', (
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['ContainsFareRule'])

        # Adding model 'RouteFareRule'
        db.create_table('gtfs_routefarerule', (
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Route'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['RouteFareRule'])

        # Adding model 'TransferType'
        db.create_table('gtfs_transfertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gtfs', ['TransferType'])

        # Adding model 'OriginFareRule'
        db.create_table('gtfs_originfarerule', (
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['OriginFareRule'])

        # Adding model 'DestinationFareRule'
        db.create_table('gtfs_destinationfarerule', (
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Zone'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.FareRule'])),
        ))
        db.send_create_signal('gtfs', ['DestinationFareRule'])

        # Adding model 'RouteType'
        db.create_table('gtfs_routetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gtfs', ['RouteType'])

        # Adding model 'Arrangement'
        db.create_table('gtfs_arrangement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('gtfs', ['Arrangement'])

        # User chose to not deal with backwards NULL issues for 'FareRule.transfer_permission'
        raise RuntimeError("Cannot reverse this migration. 'FareRule.transfer_permission' and its values cannot be restored.")

        # Deleting field 'FareRule.transfers'
        db.delete_column('gtfs_farerule', 'transfers')

        # Deleting field 'FareRule.route'
        db.delete_column('gtfs_farerule', 'route_id')

        # Deleting field 'FareRule.origin'
        db.delete_column('gtfs_farerule', 'origin_id')

        # Deleting field 'FareRule.destination'
        db.delete_column('gtfs_farerule', 'destination_id')

        # Deleting field 'FareRule.contains'
        db.delete_column('gtfs_farerule', 'contains_id')

        # Renaming column for 'FareRule.payment_method' to match new field type.
        db.rename_column('gtfs_farerule', 'payment_method', 'payment_method_id')
        # Changing field 'FareRule.payment_method'
        db.alter_column('gtfs_farerule', 'payment_method_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.PaymentMethod']))

        # Renaming column for 'Transfer.transfer_type' to match new field type.
        db.rename_column('gtfs_transfer', 'transfer_type', 'transfer_type_id')
        # Changing field 'Transfer.transfer_type'
        db.alter_column('gtfs_transfer', 'transfer_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.TransferType']))

        # Changing field 'Route.short_name'
        db.alter_column('gtfs_route', 'short_name', self.gf('django.db.models.fields.TextField')())

        # Renaming column for 'Route.route_type' to match new field type.
        db.rename_column('gtfs_route', 'route_type', 'route_type_id')
        # Changing field 'Route.route_type'
        db.alter_column('gtfs_route', 'route_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.RouteType']))

        # Changing field 'Route.text_color'
        db.alter_column('gtfs_route', 'text_color', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Route.color'
        db.alter_column('gtfs_route', 'color', self.gf('django.db.models.fields.TextField')())

        # Adding field 'Stop.is_station'
        db.add_column('gtfs_stop', 'is_station', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'Stop.location_type'
        db.delete_column('gtfs_stop', 'location_type')

        # Changing field 'Stop.code'
        db.alter_column('gtfs_stop', 'code', self.gf('django.db.models.fields.TextField')())

        # Renaming column for 'StopTime.pickup_type' to match new field type.
        db.rename_column('gtfs_stoptime', 'pickup_type', 'pickup_type_id')
        # Changing field 'StopTime.pickup_type'
        db.alter_column('gtfs_stoptime', 'pickup_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['gtfs.Arrangement']))

        # Renaming column for 'StopTime.drop_off_type' to match new field type.
        db.rename_column('gtfs_stoptime', 'drop_off_type', 'drop_off_type_id')
        # Changing field 'StopTime.drop_off_type'
        db.alter_column('gtfs_stoptime', 'drop_off_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['gtfs.Arrangement']))


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
            'date': ('django.db.models.fields.DateField', [], {}),
            'exception_type': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Service']"})
        },
        'gtfs.farerule': {
            'Meta': {'object_name': 'FareRule'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Agency']"}),
            'contains': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fare_rule_contains'", 'null': 'True', 'to': "orm['gtfs.Zone']"}),
            'currency_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fare_rule_destinations'", 'null': 'True', 'to': "orm['gtfs.Zone']"}),
            'farerule_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fare_rule_origins'", 'null': 'True', 'to': "orm['gtfs.Zone']"}),
            'payment_method': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Route']", 'null': 'True'}),
            'transfer_duration': ('django.db.models.fields.IntegerField', [], {}),
            'transfers': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
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
        'gtfs.route': {
            'Meta': {'unique_together': "(('agency', 'route_id'),)", 'object_name': 'Route'},
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Agency']", 'null': 'True'}),
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
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Source']", 'null': 'True'})
        },
        'gtfs.shape': {
            'Meta': {'object_name': 'Shape'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.contrib.gis.db.models.fields.LineStringField', [], {'null': 'True'}),
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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'location_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'drop_off_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pickup_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'transfer_type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'gtfs.transferpermission': {
            'Meta': {'object_name': 'TransferPermission'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ntransfers': ('django.db.models.fields.IntegerField', [], {})
        },
        'gtfs.trip': {
            'Meta': {'unique_together': "(('service', 'trip_id'), ('route', 'trip_id'))", 'object_name': 'Trip'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Block']", 'null': 'True'}),
            'direction_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'headsign': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
