# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CalUser'
        db.create_table('cal_caluser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_netid', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('user_email', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('user_firstname', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('user_lastname', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('user_pustatus', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('user_dept', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('user_last_login', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user_privacy_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_reminders_requested', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user_notify_invitation', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cal', ['CalUser'])

        # Adding M2M table for field user_recently_viewed_events on 'CalUser'
        db.create_table('cal_caluser_user_recently_viewed_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('caluser', models.ForeignKey(orm['cal.caluser'], null=False)),
            ('event', models.ForeignKey(orm['cal.event'], null=False))
        ))
        db.create_unique('cal_caluser_user_recently_viewed_events', ['caluser_id', 'event_id'])

        # Adding model 'EventFeature'
        db.create_table('cal_eventfeature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feature_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('feature_icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('cal', ['EventFeature'])

        # Adding model 'EventCategory'
        db.create_table('cal_eventcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cal', ['EventCategory'])

        # Adding model 'EventCluster'
        db.create_table('cal_eventcluster', (
            ('cluster_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cluster_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cluster_description', self.gf('django.db.models.fields.TextField')()),
            ('cluster_date_time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('cluster_user_created', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.CalUser'])),
            ('cluster_image', self.gf('stdimage.fields.StdImageField')(blank=True, max_length=100, upload_to='cal/Images', thumbnail_size={'width': 260, 'force': None, 'height': 520}, size={'width': 560, 'force': None, 'height': 800})),
            ('cluster_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.EventCategory'])),
            ('cluster_rsvp_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cluster_board_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cluster_notify_boardpost', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cluster_parent_subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.WebcalSubscription'], null=True)),
        ))
        db.send_create_signal('cal', ['EventCluster'])

        # Adding M2M table for field cluster_features on 'EventCluster'
        db.create_table('cal_eventcluster_cluster_features', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('eventcluster', models.ForeignKey(orm['cal.eventcluster'], null=False)),
            ('eventfeature', models.ForeignKey(orm['cal.eventfeature'], null=False))
        ))
        db.create_unique('cal_eventcluster_cluster_features', ['eventcluster_id', 'eventfeature_id'])

        # Adding model 'Event'
        db.create_table('cal_event', (
            ('event_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_date_time_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('event_date_time_last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('event_user_last_modified', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.CalUser'])),
            ('event_subtitle', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('event_subdescription', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('event_date_time_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_date_time_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_location', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('event_location_details', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('event_date_rsvp_deadline', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('event_max_attendance', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('event_attendee_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('event_cluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.EventCluster'])),
            ('event_cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('event_webcal_uid', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True, null=True)),
        ))
        db.send_create_signal('cal', ['Event'])

        # Adding model 'BoardMessage'
        db.create_table('cal_boardmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('boardmessage_eventcluster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.EventCluster'])),
            ('boardmessage_time_posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('boardmessage_poster', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.CalUser'])),
            ('boardmessage_title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('boardmessage_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('cal', ['BoardMessage'])

        # Adding model 'RSVP'
        db.create_table('cal_rsvp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rsvp_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='CalUser.rsvp_user_set', to=orm['cal.CalUser'])),
            ('rsvp_referrer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='CalUser.rsvp_referrer_set', null=True, to=orm['cal.CalUser'])),
            ('rsvp_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.Event'])),
            ('rsvp_date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('rsvp_reminder_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rsvp_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('cal', ['RSVP'])

        # Adding model 'VisitorMessage'
        db.create_table('cal_visitormessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vm_session', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('vm_date_queued', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('vm_show_after', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('vm_from_page', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('vm_to_page', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('vm_class', self.gf('django.db.models.fields.IntegerField')()),
            ('vm_contents', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('vm_pending', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cal', ['VisitorMessage'])

        # Adding model 'UserMessage'
        db.create_table('cal_usermessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('um_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.CalUser'])),
            ('um_date_posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('um_date_read', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('um_contents', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('cal', ['UserMessage'])

        # Adding model 'View'
        db.create_table('cal_view', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('view_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.Event'])),
            ('view_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('view_viewer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.CalUser'])),
            ('view_count', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('cal', ['View'])

        # Adding model 'WebcalSubscription'
        db.create_table('cal_webcalsubscription', (
            ('webcal_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('webcal_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('webcal_title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('webcal_description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('webcal_default_location', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('webcal_default_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.EventCategory'])),
            ('webcal_user_added', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cal.CalUser'])),
            ('webcal_date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('webcal_date_last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('cal', ['WebcalSubscription'])


    def backwards(self, orm):
        
        # Deleting model 'CalUser'
        db.delete_table('cal_caluser')

        # Removing M2M table for field user_recently_viewed_events on 'CalUser'
        db.delete_table('cal_caluser_user_recently_viewed_events')

        # Deleting model 'EventFeature'
        db.delete_table('cal_eventfeature')

        # Deleting model 'EventCategory'
        db.delete_table('cal_eventcategory')

        # Deleting model 'EventCluster'
        db.delete_table('cal_eventcluster')

        # Removing M2M table for field cluster_features on 'EventCluster'
        db.delete_table('cal_eventcluster_cluster_features')

        # Deleting model 'Event'
        db.delete_table('cal_event')

        # Deleting model 'BoardMessage'
        db.delete_table('cal_boardmessage')

        # Deleting model 'RSVP'
        db.delete_table('cal_rsvp')

        # Deleting model 'VisitorMessage'
        db.delete_table('cal_visitormessage')

        # Deleting model 'UserMessage'
        db.delete_table('cal_usermessage')

        # Deleting model 'View'
        db.delete_table('cal_view')

        # Deleting model 'WebcalSubscription'
        db.delete_table('cal_webcalsubscription')


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
