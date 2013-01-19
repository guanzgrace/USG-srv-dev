# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Blurb'
        db.create_table('dvd_blurb', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('dvd', ['Blurb'])


    def backwards(self, orm):
        
        # Deleting model 'Blurb'
        db.delete_table('dvd_blurb')


    models = {
        'dvd.blurb': {
            'Meta': {'object_name': 'Blurb'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
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
