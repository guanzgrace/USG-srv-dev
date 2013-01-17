# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Club'
        db.create_table('card_clubs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('account', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='account', unique=True, null=True, to=orm['auth.User'])),
            ('check', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='check', null=True, to=orm['card.Member'])),
        ))
        db.send_create_signal('card', ['Club'])

        # Adding model 'Member'
        db.create_table('card_members', (
            ('netid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('puid', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('club', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['card.Club'], null=True, blank=True)),
            ('access', self.gf('django.db.models.fields.CharField')(default='M', max_length=20)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('card', ['Member'])

        # Adding model 'Exchange'
        db.create_table('card_exchanges', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('meal_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='meal_1', to=orm['card.Meal'])),
            ('meal_2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='meal_2', null=True, to=orm['card.Meal'])),
        ))
        db.send_create_signal('card', ['Exchange'])

        # Adding model 'Meal'
        db.create_table('card_meals', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.related.ForeignKey')(related_name='host', to=orm['card.Member'])),
            ('guest', self.gf('django.db.models.fields.related.ForeignKey')(related_name='guest', to=orm['card.Member'])),
            ('checker', self.gf('django.db.models.fields.related.ForeignKey')(related_name='checker', to=orm['card.Member'])),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 12, 22))),
            ('meal_type', self.gf('django.db.models.fields.CharField')(default='Dinner', max_length=10)),
        ))
        db.send_create_signal('card', ['Meal'])


    def backwards(self, orm):
        
        # Deleting model 'Club'
        db.delete_table('card_clubs')

        # Deleting model 'Member'
        db.delete_table('card_members')

        # Deleting model 'Exchange'
        db.delete_table('card_exchanges')

        # Deleting model 'Meal'
        db.delete_table('card_meals')


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
        'card.club': {
            'Meta': {'ordering': "['name']", 'object_name': 'Club', 'db_table': "'card_clubs'"},
            'account': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'account'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'check': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'check'", 'null': 'True', 'to': "orm['card.Member']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'card.exchange': {
            'Meta': {'ordering': "['meal_1']", 'object_name': 'Exchange', 'db_table': "'card_exchanges'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'meal_1'", 'to': "orm['card.Meal']"}),
            'meal_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'meal_2'", 'null': 'True', 'to': "orm['card.Meal']"})
        },
        'card.meal': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Meal', 'db_table': "'card_meals'"},
            'checker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checker'", 'to': "orm['card.Member']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 12, 22)'}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'guest'", 'to': "orm['card.Member']"}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'host'", 'to': "orm['card.Member']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal_type': ('django.db.models.fields.CharField', [], {'default': "'Dinner'", 'max_length': '10'})
        },
        'card.member': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Member', 'db_table': "'card_members'"},
            'access': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '20'}),
            'club': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['card.Club']", 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'netid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'primary_key': 'True'}),
            'puid': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['card']
