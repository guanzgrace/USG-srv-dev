# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Post'
        db.create_table('storage_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 22, 14, 20, 12, 434861))),
        ))
        db.send_create_signal('storage', ['Post'])

        # Adding model 'DropoffPickupTime'
        db.create_table('storage_dropoffpickuptime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slot_id', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('dropoff_date', self.gf('django.db.models.fields.DateField')()),
            ('dropoff_time_start', self.gf('django.db.models.fields.TimeField')()),
            ('dropoff_time_end', self.gf('django.db.models.fields.TimeField')()),
            ('pickup_date', self.gf('django.db.models.fields.DateField')()),
            ('pickup_time_start', self.gf('django.db.models.fields.TimeField')()),
            ('pickup_time_end', self.gf('django.db.models.fields.TimeField')()),
            ('n_boxes_total', self.gf('django.db.models.fields.IntegerField')()),
            ('n_boxes_bought', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('storage', ['DropoffPickupTime'])

        # Adding model 'UnpaidOrder'
        db.create_table('storage_unpaidorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unpaid_order', to=orm['auth.User'])),
            ('cell_number', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('dropoff_pickup_time', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unpaid_order', to=orm['storage.DropoffPickupTime'])),
            ('proxy_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('proxy_email', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('n_boxes_bought', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('invoice_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('signature', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('storage', ['UnpaidOrder'])

        # Adding model 'Order'
        db.create_table('storage_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order', unique=True, to=orm['auth.User'])),
            ('cell_number', self.gf('django.db.models.fields.CharField')(max_length=14)),
            ('dropoff_pickup_time', self.gf('django.db.models.fields.related.ForeignKey')(related_name='order', to=orm['storage.DropoffPickupTime'])),
            ('proxy_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('proxy_email', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('n_boxes_bought', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('invoice_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('signature', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('bool_picked_empty', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('n_boxes_dropped', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2, blank=True)),
            ('n_boxes_picked', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2, blank=True)),
        ))
        db.send_create_signal('storage', ['Order'])


    def backwards(self, orm):
        
        # Deleting model 'Post'
        db.delete_table('storage_post')

        # Deleting model 'DropoffPickupTime'
        db.delete_table('storage_dropoffpickuptime')

        # Deleting model 'UnpaidOrder'
        db.delete_table('storage_unpaidorder')

        # Deleting model 'Order'
        db.delete_table('storage_order')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'storage.dropoffpickuptime': {
            'Meta': {'object_name': 'DropoffPickupTime'},
            'dropoff_date': ('django.db.models.fields.DateField', [], {}),
            'dropoff_time_end': ('django.db.models.fields.TimeField', [], {}),
            'dropoff_time_start': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'n_boxes_bought': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'n_boxes_total': ('django.db.models.fields.IntegerField', [], {}),
            'pickup_date': ('django.db.models.fields.DateField', [], {}),
            'pickup_time_end': ('django.db.models.fields.TimeField', [], {}),
            'pickup_time_start': ('django.db.models.fields.TimeField', [], {}),
            'slot_id': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'storage.order': {
            'Meta': {'object_name': 'Order'},
            'bool_picked_empty': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cell_number': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'dropoff_pickup_time': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': "orm['storage.DropoffPickupTime']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'n_boxes_bought': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'n_boxes_dropped': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2', 'blank': 'True'}),
            'n_boxes_picked': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2', 'blank': 'True'}),
            'proxy_email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'proxy_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'signature': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'storage.post': {
            'Meta': {'object_name': 'Post'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 22, 14, 20, 12, 434861)'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'storage.unpaidorder': {
            'Meta': {'object_name': 'UnpaidOrder'},
            'cell_number': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'dropoff_pickup_time': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unpaid_order'", 'to': "orm['storage.DropoffPickupTime']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'n_boxes_bought': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'proxy_email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'proxy_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'signature': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unpaid_order'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['storage']
