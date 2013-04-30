# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Order', fields ['user']
        db.delete_unique('storage_order', ['user_id'])

        # Adding field 'Order.year'
        db.add_column('storage_order', 'year',
                      self.gf('django.db.models.fields.IntegerField')(default=2012),
                      keep_default=False)

        # Adding field 'DropoffPickupTime.year'
        db.add_column('storage_dropoffpickuptime', 'year',
                      self.gf('django.db.models.fields.IntegerField')(default=2012),
                      keep_default=False)

        # Adding field 'UnpaidOrder.year'
        db.add_column('storage_unpaidorder', 'year',
                      self.gf('django.db.models.fields.IntegerField')(default=2012),
                      keep_default=False)

        # Adding field 'Post.visible'
        db.add_column('storage_post', 'visible',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Order.year'
        db.delete_column('storage_order', 'year')

        # Adding unique constraint on 'Order', fields ['user']
        db.create_unique('storage_order', ['user_id'])

        # Deleting field 'DropoffPickupTime.year'
        db.delete_column('storage_dropoffpickuptime', 'year')

        # Deleting field 'UnpaidOrder.year'
        db.delete_column('storage_unpaidorder', 'year')

        # Deleting field 'Post.visible'
        db.delete_column('storage_post', 'visible')


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
            'slot_id': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2012'})
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order'", 'to': "orm['auth.User']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2012'})
        },
        'storage.post': {
            'Meta': {'object_name': 'Post'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 17, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unpaid_order'", 'to': "orm['auth.User']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2012'})
        }
    }

    complete_apps = ['storage']