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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('abbr_name', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('category', self.gf('adminsortable.fields.SortableForeignKey')(to=orm['www.Category'])),
            ('featured_index', self.gf('django.db.models.fields.IntegerField')(unique=True, null=True, blank=True)),
            ('n_views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('screenshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('founder_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
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
            'abbr_name': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'category': ('adminsortable.fields.SortableForeignKey', [], {'to': "orm['www.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'featured_index': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'founder_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'n_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'screenshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
