# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SocUser'
        db.create_table('pam_socuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('netid', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('pustatus', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('puclassyear', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('officer_at', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pam.Club'], null=True, blank=True)),
            ('is_president', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('pam', ['SocUser'])

        # Adding model 'Club'
        db.create_table('pam_club', (
            ('club_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('about', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('left_offset', self.gf('django.db.models.fields.IntegerField')()),
            ('top_offset', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('picture', self.gf('stdimage.fields.StdImageField')(blank=True, max_length=100, null=True, upload_to='pam/images/picture', size={'width': 300, 'force': None, 'height': 196})),
            ('active', self.gf('stdimage.fields.StdImageField')(max_length=100, null=True, upload_to='pam/images/active', blank=True)),
            ('active_selected', self.gf('stdimage.fields.StdImageField')(max_length=100, null=True, upload_to='pam/images/active_selected', blank=True)),
            ('inactive', self.gf('stdimage.fields.StdImageField')(max_length=100, null=True, upload_to='pam/images/inactive', blank=True)),
            ('inactive_selected', self.gf('stdimage.fields.StdImageField')(max_length=100, null=True, upload_to='pam/images/inactive_selected', blank=True)),
        ))
        db.send_create_signal('pam', ['Club'])

        # Adding model 'Event'
        db.create_table('pam_event', (
            ('event_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pam.Club'])),
            ('entry', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('entry_description', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('poster', self.gf('stdimage.fields.StdImageField')(thumbnail_size={'width': 250, 'force': None, 'height': 375}, upload_to='pam/images/events_posters/', max_length=100, blank=True, null=True, size={'width': 400, 'force': None, 'height': 600})),
            ('time_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('pam', ['Event'])


    def backwards(self, orm):
        
        # Deleting model 'SocUser'
        db.delete_table('pam_socuser')

        # Deleting model 'Club'
        db.delete_table('pam_club')

        # Deleting model 'Event'
        db.delete_table('pam_event')


    models = {
        'pam.club': {
            'Meta': {'object_name': 'Club'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('stdimage.fields.StdImageField', [], {'max_length': '100', 'null': 'True', 'upload_to': "'pam/images/active'", 'blank': 'True'}),
            'active_selected': ('stdimage.fields.StdImageField', [], {'max_length': '100', 'null': 'True', 'upload_to': "'pam/images/active_selected'", 'blank': 'True'}),
            'club_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inactive': ('stdimage.fields.StdImageField', [], {'max_length': '100', 'null': 'True', 'upload_to': "'pam/images/inactive'", 'blank': 'True'}),
            'inactive_selected': ('stdimage.fields.StdImageField', [], {'max_length': '100', 'null': 'True', 'upload_to': "'pam/images/inactive_selected'", 'blank': 'True'}),
            'left_offset': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'picture': ('stdimage.fields.StdImageField', [], {'blank': 'True', 'max_length': '100', 'null': 'True', 'upload_to': "'pam/images/picture'", 'size': "{'width': 300, 'force': None, 'height': 196}"}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'top_offset': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'pam.event': {
            'Meta': {'object_name': 'Event'},
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pam.Club']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'entry': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'entry_description': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'event_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poster': ('stdimage.fields.StdImageField', [], {'thumbnail_size': "{'width': 250, 'force': None, 'height': 375}", 'upload_to': "'pam/images/events_posters/'", 'max_length': '100', 'blank': 'True', 'null': 'True', 'size': "{'width': 400, 'force': None, 'height': 600}"}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        'pam.socuser': {
            'Meta': {'object_name': 'SocUser'},
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_president': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'netid': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'officer_at': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pam.Club']", 'null': 'True', 'blank': 'True'}),
            'puclassyear': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pustatus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['pam']
