# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DVD'
        db.create_table('dvd_dvd', (
            ('dvd_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sortname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('amountTotal', self.gf('django.db.models.fields.IntegerField')()),
            ('amountLeft', self.gf('django.db.models.fields.IntegerField')()),
            ('imdbID', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('timesRented', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('dvd', ['DVD'])

        # Adding model 'Rental'
        db.create_table('dvd_rental', (
            ('rentalID', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('netid', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('dvd', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dvd.DVD'])),
            ('dateRented', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('dateDue', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('dateReturned', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('dvd', ['Rental'])

        # Adding model 'Notice'
        db.create_table('dvd_notice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('netid', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('dvd', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dvd.DVD'])),
        ))
        db.send_create_signal('dvd', ['Notice'])


    def backwards(self, orm):
        
        # Deleting model 'DVD'
        db.delete_table('dvd_dvd')

        # Deleting model 'Rental'
        db.delete_table('dvd_rental')

        # Deleting model 'Notice'
        db.delete_table('dvd_notice')


    models = {
        'dvd.dvd': {
            'Meta': {'object_name': 'DVD'},
            'amountLeft': ('django.db.models.fields.IntegerField', [], {}),
            'amountTotal': ('django.db.models.fields.IntegerField', [], {}),
            'dvd_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdbID': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sortname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timesRented': ('django.db.models.fields.IntegerField', [], {})
        },
        'dvd.notice': {
            'Meta': {'object_name': 'Notice'},
            'dvd': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dvd.DVD']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'netid': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        'dvd.rental': {
            'Meta': {'object_name': 'Rental'},
            'dateDue': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'dateRented': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'dateReturned': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dvd': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dvd.DVD']"}),
            'netid': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'rentalID': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['dvd']
