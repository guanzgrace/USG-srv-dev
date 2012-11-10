# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('www_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('www', ['Category'])

        # Adding model 'App'
        db.create_table('www_app', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('long_description', self.gf('django.db.models.fields.TextField')()),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('slideshow_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('number_of_views', self.gf('django.db.models.fields.IntegerField')()),
            ('category', self.gf('adminsortable.fields.SortableForeignKey')(to=orm['www.Category'])),
            ('slideshow_index', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('www', ['App'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('www_category')

        # Deleting model 'App'
        db.delete_table('www_app')


    models = {
        'www.app': {
            'Meta': {'ordering': "['category__order', 'order']", 'object_name': 'App'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'category': ('adminsortable.fields.SortableForeignKey', [], {'to': "orm['www.Category']"}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_description': ('django.db.models.fields.TextField', [], {}),
            'number_of_views': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'slideshow_index': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slideshow_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'www.category': {
            'Meta': {'ordering': "['order']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'})
        }
    }

    complete_apps = ['www']
