# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Student'
        db.create_table(u'enroll_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('netID', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('blocks', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=5000, blank=True)),
        ))
        db.send_create_signal(u'enroll', ['Student'])

        # Adding model 'Instructor'
        db.create_table(u'enroll_instructor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('netID', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('hours', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'enroll', ['Instructor'])

        # Adding model 'Course'
        db.create_table(u'enroll_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('courseID', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('min_enroll', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('max_enroll', self.gf('django.db.models.fields.IntegerField')(default=200)),
            ('cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('room', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('blocks', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=5000)),
            ('schedule', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'enroll', ['Course'])

        # Adding M2M table for field other_section on 'Course'
        m2m_table_name = db.shorten_name(u'enroll_course_other_section')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_course', models.ForeignKey(orm[u'enroll.course'], null=False)),
            ('to_course', models.ForeignKey(orm[u'enroll.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_course_id', 'to_course_id'])

        # Adding M2M table for field instructors on 'Course'
        m2m_table_name = db.shorten_name(u'enroll_course_instructors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'enroll.course'], null=False)),
            ('instructor', models.ForeignKey(orm[u'enroll.instructor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'instructor_id'])

        # Adding model 'Registration'
        db.create_table(u'enroll_registration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enroll.Student'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enroll.Course'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'enroll', ['Registration'])


    def backwards(self, orm):
        # Deleting model 'Student'
        db.delete_table(u'enroll_student')

        # Deleting model 'Instructor'
        db.delete_table(u'enroll_instructor')

        # Deleting model 'Course'
        db.delete_table(u'enroll_course')

        # Removing M2M table for field other_section on 'Course'
        db.delete_table(db.shorten_name(u'enroll_course_other_section'))

        # Removing M2M table for field instructors on 'Course'
        db.delete_table(db.shorten_name(u'enroll_course_instructors'))

        # Deleting model 'Registration'
        db.delete_table(u'enroll_registration')


    models = {
        u'enroll.course': {
            'Meta': {'object_name': 'Course'},
            'blocks': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '5000'}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'courseID': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['enroll.Instructor']", 'symmetrical': 'False'}),
            'max_enroll': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'min_enroll': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'other_section': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'other_section_rel_+'", 'blank': 'True', 'to': u"orm['enroll.Course']"}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'schedule': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['enroll.Student']", 'through': u"orm['enroll.Registration']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'enroll.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'netID': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        u'enroll.registration': {
            'Meta': {'object_name': 'Registration'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['enroll.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['enroll.Student']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'enroll.student': {
            'Meta': {'object_name': 'Student'},
            'blocks': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '5000', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'netID': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        }
    }

    complete_apps = ['enroll']