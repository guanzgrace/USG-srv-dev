# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Office'
        db.create_table('elections_office', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('freshman_eligible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sophomore_eligible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('junior_eligible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('freshman_vote', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sophomore_vote', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('junior_vote', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('senior_vote', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('elections', ['Office'])

        # Adding model 'Candidate'
        db.create_table('elections_candidate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('netid', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('office', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['elections.Office'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('statement', self.gf('django.db.models.fields.TextField')()),
            ('headshot', self.gf('stdimage.fields.StdImageField')(max_length=100, upload_to='elections/upload/', thumbnail_size={'width': 125, 'force': None, 'height': 350}, size={'width': 350, 'force': None, 'height': 225})),
            ('election', self.gf('django.db.models.fields.related.ForeignKey')(related_name='election', to=orm['elections.Election'])),
        ))
        db.send_create_signal('elections', ['Candidate'])

        # Adding model 'Election'
        db.create_table('elections_election', (
            ('electionID', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('deadline', self.gf('django.db.models.fields.DateTimeField')()),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('elections', ['Election'])

        # Adding M2M table for field offices on 'Election'
        db.create_table('elections_election_offices', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('election', models.ForeignKey(orm['elections.election'], null=False)),
            ('office', models.ForeignKey(orm['elections.office'], null=False))
        ))
        db.create_unique('elections_election_offices', ['election_id', 'office_id'])

        # Adding model 'Runoff'
        db.create_table('elections_runoff', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('election', self.gf('django.db.models.fields.related.ForeignKey')(related_name='runoff_election', to=orm['elections.Election'])),
        ))
        db.send_create_signal('elections', ['Runoff'])

        # Adding M2M table for field candidates on 'Runoff'
        db.create_table('elections_runoff_candidates', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('runoff', models.ForeignKey(orm['elections.runoff'], null=False)),
            ('candidate', models.ForeignKey(orm['elections.candidate'], null=False))
        ))
        db.create_unique('elections_runoff_candidates', ['runoff_id', 'candidate_id'])


    def backwards(self, orm):
        
        # Deleting model 'Office'
        db.delete_table('elections_office')

        # Deleting model 'Candidate'
        db.delete_table('elections_candidate')

        # Deleting model 'Election'
        db.delete_table('elections_election')

        # Removing M2M table for field offices on 'Election'
        db.delete_table('elections_election_offices')

        # Deleting model 'Runoff'
        db.delete_table('elections_runoff')

        # Removing M2M table for field candidates on 'Runoff'
        db.delete_table('elections_runoff_candidates')


    models = {
        'elections.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'election': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'election'", 'to': "orm['elections.Election']"}),
            'headshot': ('stdimage.fields.StdImageField', [], {'max_length': '100', 'upload_to': "'elections/upload/'", 'thumbnail_size': "{'width': 125, 'force': None, 'height': 350}", 'size': "{'width': 350, 'force': None, 'height': 225}"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'netid': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'office': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.Office']"}),
            'statement': ('django.db.models.fields.TextField', [], {}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'elections.election': {
            'Meta': {'object_name': 'Election'},
            'deadline': ('django.db.models.fields.DateTimeField', [], {}),
            'electionID': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'offices': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['elections.Office']", 'symmetrical': 'False'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'elections.office': {
            'Meta': {'object_name': 'Office'},
            'freshman_eligible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'freshman_vote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'junior_eligible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'junior_vote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'senior_vote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sophomore_eligible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sophomore_vote': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'elections.runoff': {
            'Meta': {'object_name': 'Runoff'},
            'candidates': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'candidate'", 'symmetrical': 'False', 'to': "orm['elections.Candidate']"}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'runoff_election'", 'to': "orm['elections.Election']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['elections']
