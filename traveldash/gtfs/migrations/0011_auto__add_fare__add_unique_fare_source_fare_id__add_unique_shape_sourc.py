# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Fare'
        db.create_table('gtfs_fare', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Source'], null=True)),
            ('fare_id', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('currency_type', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('payment_method', self.gf('django.db.models.fields.IntegerField')()),
            ('transfers', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('transfer_duration', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('gtfs', ['Fare'])

        # Adding unique constraint on 'Fare', fields ['source', 'fare_id']
        db.create_unique('gtfs_fare', ['source_id', 'fare_id'])

        # Adding unique constraint on 'Shape', fields ['source', 'shape_id']
        db.create_unique('gtfs_shape', ['source_id', 'shape_id'])

        # Adding field 'Zone.source'
        db.add_column('gtfs_zone', 'source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gtfs.Source'], null=True), keep_default=False)

        # Adding unique constraint on 'Zone', fields ['source', 'zone_id']
        db.create_unique('gtfs_zone', ['source_id', 'zone_id'])

        # Deleting field 'FareRule.payment_method'
        db.delete_column('gtfs_farerule', 'payment_method')

        # Deleting field 'FareRule.price'
        db.delete_column('gtfs_farerule', 'price')

        # Deleting field 'FareRule.currency_type'
        db.delete_column('gtfs_farerule', 'currency_type')

        # Deleting field 'FareRule.transfer_duration'
        db.delete_column('gtfs_farerule', 'transfer_duration')

        # Deleting field 'FareRule.transfers'
        db.delete_column('gtfs_farerule', 'transfers')

        # Deleting field 'FareRule.farerule_id'
        db.delete_column('gtfs_farerule', 'farerule_id')

        # Deleting field 'FareRule.agency'
        db.delete_column('gtfs_farerule', 'agency_id')

        # Adding field 'FareRule.fare'
        db.add_column('gtfs_farerule', 'fare', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['gtfs.Fare']), keep_default=False)

    def backwards(self, orm):

        # Removing unique constraint on 'Zone', fields ['source', 'zone_id']
        db.delete_unique('gtfs_zone', ['source_id', 'zone_id'])

        # Removing unique constraint on 'Shape', fields ['source', 'shape_id']
        db.delete_unique('gtfs_shape', ['source_id', 'shape_id'])

        # Removing unique constraint on 'Fare', fields ['source', 'fare_id']
        db.delete_unique('gtfs_fare', ['source_id', 'fare_id'])

        # Deleting model 'Fare'
        db.delete_table('gtfs_fare')

        # Deleting field 'Zone.source'
        db.delete_column('gtfs_zone', 'source_id')

        # User chose to not deal with backwards NULL issues for 'FareRule.payment_method'
        raise RuntimeError("Cannot reverse this migration. 'FareRule.payment_method' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'FareRule.price'
        raise RuntimeError("Cannot reverse this migration. 'FareRule.price' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'FareRule.currency_type'
        raise RuntimeError("Cannot reverse this migration. 'FareRule.currency_type' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'FareRule.transfer_duration'
        raise RuntimeError("Cannot reverse this migration. 'FareRule.transfer_duration' and its values cannot be restored.")

        # Adding field 'FareRule.transfers'
        db.add_column('gtfs_farerule', 'transfers', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'FareRule.farerule_id'
        raise RuntimeError("Cannot reverse this migration. 'FareRule.farerule_id' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'FareRule.agency'
        raise RuntimeError("Cannot reverse this migration. 'FareRule.agency' and its values cannot be restored.")

        # Deleting field 'FareRule.fare'
        db.delete_column('gtfs_farerule', 'fare_id')

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
            'exception_type': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Service']"})
        },
        'gtfs.fare': {
            'Meta': {'unique_together': "(('source', 'fare_id'),)", 'object_name': 'Fare'},
            'currency_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'fare_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_method': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Source']", 'null': 'True'}),
            'transfer_duration': ('django.db.models.fields.IntegerField', [], {}),
            'transfers': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'gtfs.farerule': {
            'Meta': {'object_name': 'FareRule'},
            'contains': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fare_rule_contains'", 'null': 'True', 'to': "orm['gtfs.Zone']"}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fare_rule_destinations'", 'null': 'True', 'to': "orm['gtfs.Zone']"}),
            'fare': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Fare']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fare_rule_origins'", 'null': 'True', 'to': "orm['gtfs.Zone']"}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Route']", 'null': 'True'})
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
            'Meta': {'unique_together': "(('source', 'shape_id'),)", 'object_name': 'Shape'},
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
            'location_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
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
        'gtfs.trip': {
            'Meta': {'unique_together': "(('service', 'trip_id'), ('route', 'trip_id'))", 'object_name': 'Trip'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Block']", 'null': 'True'}),
            'direction_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'headsign': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Route']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Service']"}),
            'shape': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Shape']", 'null': 'True'}),
            'short_name': ('django.db.models.fields.TextField', [], {}),
            'trip_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'gtfs.zone': {
            'Meta': {'unique_together': "(('source', 'zone_id'),)", 'object_name': 'Zone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gtfs.Source']", 'null': 'True'}),
            'zone_id': ('django.db.models.fields.TextField', [], {'max_length': '20', 'db_index': 'True'})
        }
    }

    complete_apps = ['gtfs']
