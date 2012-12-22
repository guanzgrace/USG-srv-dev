# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Post'
        db.create_table('ccc_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 22, 14, 49, 43, 432166))),
            ('in_blog', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('ccc', ['Post'])

        # Adding model 'GroupHours'
        db.create_table('ccc_grouphours', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
            ('month', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('ccc', ['GroupHours'])

        # Adding model 'LogCluster'
        db.create_table('ccc_logcluster', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ccc.ProjectOrOrganization'])),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('res_college', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('eating_club', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logcluster', to=orm['auth.User'])),
        ))
        db.send_create_signal('ccc', ['LogCluster'])

        # Adding model 'Award'
        db.create_table('ccc_award', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='award', to=orm['auth.User'])),
            ('hours', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('ccc', ['Award'])

        # Adding model 'ProjectRequest'
        db.create_table('ccc_projectrequest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('coordinator_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('coordinator_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projectrequest', to=orm['auth.User'])),
        ))
        db.send_create_signal('ccc', ['ProjectRequest'])

        # Adding model 'ProjectOrOrganization'
        db.create_table('ccc_projectororganization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
        ))
        db.send_create_signal('ccc', ['ProjectOrOrganization'])


    def backwards(self, orm):
        
        # Deleting model 'Post'
        db.delete_table('ccc_post')

        # Deleting model 'GroupHours'
        db.delete_table('ccc_grouphours')

        # Deleting model 'LogCluster'
        db.delete_table('ccc_logcluster')

        # Deleting model 'Award'
        db.delete_table('ccc_award')

        # Deleting model 'ProjectRequest'
        db.delete_table('ccc_projectrequest')

        # Deleting model 'ProjectOrOrganization'
        db.delete_table('ccc_projectororganization')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'ccc.award': {
            'Meta': {'object_name': 'Award'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'award'", 'to': "orm['auth.User']"})
        },
        'ccc.grouphours': {
            'Meta': {'ordering': "['month']", 'object_name': 'GroupHours'},
            'group': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.DateField', [], {})
        },
        'ccc.logcluster': {
            'Meta': {'object_name': 'LogCluster'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'eating_club': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'hours': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ccc.ProjectOrOrganization']"}),
            'res_college': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logcluster'", 'to': "orm['auth.User']"}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'ccc.post': {
            'Meta': {'object_name': 'Post'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_blog': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 22, 14, 49, 43, 432166)'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'ccc.projectororganization': {
            'Meta': {'ordering': "['name']", 'object_name': 'ProjectOrOrganization'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        'ccc.projectrequest': {
            'Meta': {'object_name': 'ProjectRequest'},
            'coordinator_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'coordinator_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projectrequest'", 'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['ccc']
