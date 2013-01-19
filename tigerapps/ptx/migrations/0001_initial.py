# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Course'
        db.create_table('ptx_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dept', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('num', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('ptx', ['Course'])

        # Adding unique constraint on 'Course', fields ['dept', 'num']
        db.create_unique('ptx_course', ['dept', 'num'])

        # Adding model 'Book'
        db.create_table('ptx_book', (
            ('isbn13', self.gf('django.db.models.fields.CharField')(max_length=13, primary_key=True)),
            ('isbn10', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('edition', self.gf('django.db.models.fields.CharField')(max_length=512, null=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('list_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2)),
            ('imagename', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('amazon_info', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('amazon_img', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('labyrinth_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal('ptx', ['Book'])

        # Adding M2M table for field course on 'Book'
        db.create_table('ptx_book_course', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['ptx.book'], null=False)),
            ('course', models.ForeignKey(orm['ptx.course'], null=False))
        ))
        db.create_unique('ptx_book_course', ['book_id', 'course_id'])

        # Adding model 'User'
        db.create_table('ptx_user', (
            ('net_id', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('dorm_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dorm_room', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ratings_up', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ratings_down', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('dollars_spent', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=10, decimal_places=2)),
            ('dollars_earned', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal('ptx', ['User'])

        # Adding model 'Offer'
        db.create_table('ptx_offer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ptx.Book'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ptx.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('allow_bids', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_rated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('semester', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('date_open', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_pending', self.gf('django.db.models.fields.DateField')(null=True)),
            ('date_closed', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal('ptx', ['Offer'])

        # Adding model 'Request'
        db.create_table('ptx_request', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ptx.User'])),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ptx.Book'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='o', max_length='1')),
            ('maxprice', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=10, decimal_places=2)),
            ('date_open', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('date_pending', self.gf('django.db.models.fields.DateField')(null=True)),
            ('date_closed', self.gf('django.db.models.fields.DateField')(null=True)),
            ('offer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ptx.Offer'], null=True)),
            ('has_rated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ptx', ['Request'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Course', fields ['dept', 'num']
        db.delete_unique('ptx_course', ['dept', 'num'])

        # Deleting model 'Course'
        db.delete_table('ptx_course')

        # Deleting model 'Book'
        db.delete_table('ptx_book')

        # Removing M2M table for field course on 'Book'
        db.delete_table('ptx_book_course')

        # Deleting model 'User'
        db.delete_table('ptx_user')

        # Deleting model 'Offer'
        db.delete_table('ptx_offer')

        # Deleting model 'Request'
        db.delete_table('ptx_request')


    models = {
        'ptx.book': {
            'Meta': {'object_name': 'Book'},
            'amazon_img': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'amazon_info': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'course': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['ptx.Course']", 'symmetrical': 'False'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'edition': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True'}),
            'imagename': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'isbn10': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'isbn13': ('django.db.models.fields.CharField', [], {'max_length': '13', 'primary_key': 'True'}),
            'labyrinth_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'list_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'ptx.course': {
            'Meta': {'unique_together': "(('dept', 'num'),)", 'object_name': 'Course'},
            'dept': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {})
        },
        'ptx.offer': {
            'Meta': {'object_name': 'Offer'},
            'allow_bids': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ptx.Book']"}),
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'date_closed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_open': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_pending': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'has_rated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ptx.User']"}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'ptx.request': {
            'Meta': {'object_name': 'Request'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ptx.Book']"}),
            'date_closed': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_open': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_pending': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'has_rated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maxprice': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '10', 'decimal_places': '2'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ptx.Offer']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'o'", 'max_length': "'1'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ptx.User']"})
        },
        'ptx.user': {
            'Meta': {'object_name': 'User'},
            'dollars_earned': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'dollars_spent': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2'}),
            'dorm_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dorm_room': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'net_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'ratings_down': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ratings_up': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['ptx']
