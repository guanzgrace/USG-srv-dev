# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding M2M table for field cluster_categories on 'EventCluster'
        db.create_table('cal_eventcluster_cluster_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('eventcluster', models.ForeignKey(orm['cal.eventcluster'], null=False)),
            ('eventcategory', models.ForeignKey(orm['cal.eventcategory'], null=False))
        ))
        db.create_unique('cal_eventcluster_cluster_categories', ['eventcluster_id', 'eventcategory_id'])

        if not db.dry_run:
            for obj in orm.EventCluster.objects.all():
                obj.cluster_categories.add(obj.cluster_category)
                obj.save()

    def backwards(self, orm):
        
        # Removing M2M table for field cluster_categories on 'EventCluster'
        db.delete_table('cal_eventcluster_cluster_categories')


    models = {
        'cal.boardmessage': {
            'Meta': {'object_name': 'BoardMessage'},
            'boardmessage_eventcluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.EventCluster']"}),
            'boardmessage_poster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.CalUser']"}),
            'boardmessage_text': ('django.db.models.fields.TextField', [], {}),
            'boardmessage_time_posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'boardmessage_title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cal.caluser': {
            'Meta': {'object_name': 'CalUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_dept': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'user_email': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user_firstname': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'user_last_login': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user_lastname': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'user_netid': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'user_notify_invitation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_privacy_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_pustatus': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user_recently_viewed_events': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cal.Event']", 'symmetrical': 'False', 'blank': 'True'}),
            'user_reminders_requested': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'cal.event': {
            'Meta': {'object_name': 'Event'},
            'event_attendee_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'event_cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'event_cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.EventCluster']"}),
            'event_date_rsvp_deadline': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'event_date_time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_date_time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'event_date_time_last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'event_date_time_start': ('django.db.models.fields.DateTimeField', [], {}),
            'event_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'event_location': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'event_location_details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'event_max_attendance': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'event_subdescription': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'event_user_last_modified': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.CalUser']"}),
            'event_webcal_uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True'})
        },
        'cal.eventcategory': {
            'Meta': {'object_name': 'EventCategory'},
            'category_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cal.eventcluster': {
            'Meta': {'object_name': 'EventCluster'},
            'cluster_board_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cluster_categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'Tag'", 'symmetrical': 'False', 'to': "orm['cal.EventCategory']"}),
            'cluster_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.EventCategory']"}),
            'cluster_date_time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cluster_description': ('django.db.models.fields.TextField', [], {}),
            'cluster_features': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cal.EventFeature']", 'symmetrical': 'False', 'blank': 'True'}),
            'cluster_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'cluster_image': ('stdimage.fields.StdImageField', [], {'blank': 'True', 'max_length': '100', 'upload_to': "'cal/Images'", 'thumbnail_size': "{'width': 260, 'force': None, 'height': 520}", 'size': "{'width': 560, 'force': None, 'height': 800}"}),
            'cluster_notify_boardpost': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cluster_parent_subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.WebcalSubscription']", 'null': 'True'}),
            'cluster_rsvp_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cluster_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cluster_user_created': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.CalUser']"})
        },
        'cal.eventfeature': {
            'Meta': {'object_name': 'EventFeature'},
            'feature_icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'feature_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cal.rsvp': {
            'Meta': {'object_name': 'RSVP'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rsvp_date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'rsvp_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.Event']"}),
            'rsvp_referrer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'CalUser.rsvp_referrer_set'", 'null': 'True', 'to': "orm['cal.CalUser']"}),
            'rsvp_reminder_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rsvp_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'rsvp_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'CalUser.rsvp_user_set'", 'to': "orm['cal.CalUser']"})
        },
        'cal.usermessage': {
            'Meta': {'object_name': 'UserMessage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'um_contents': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'um_date_posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'um_date_read': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'um_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.CalUser']"})
        },
        'cal.view': {
            'Meta': {'object_name': 'View'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'view_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'view_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'view_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.Event']"}),
            'view_viewer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.CalUser']"})
        },
        'cal.visitormessage': {
            'Meta': {'object_name': 'VisitorMessage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vm_class': ('django.db.models.fields.IntegerField', [], {}),
            'vm_contents': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'vm_date_queued': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'vm_from_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'vm_pending': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vm_session': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'vm_show_after': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'vm_to_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'cal.webcalsubscription': {
            'Meta': {'object_name': 'WebcalSubscription'},
            'webcal_date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'webcal_date_last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'webcal_default_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.EventCategory']"}),
            'webcal_default_location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'webcal_description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'webcal_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'webcal_title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'webcal_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'webcal_user_added': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cal.CalUser']"})
        }
    }

    complete_apps = ['cal']
