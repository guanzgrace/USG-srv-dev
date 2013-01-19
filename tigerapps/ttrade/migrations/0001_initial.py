# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Listing'
        db.create_table('ttrade_listing', (
            ('listingID', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('listingType', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Lister', to=orm['auth.User'])),
            ('picture', self.gf('stdimage.fields.StdImageField')(blank=True, max_length=100, upload_to='ttrade/images/upload/', size={'width': 560, 'force': None, 'height': 800})),
            ('posted', self.gf('django.db.models.fields.DateTimeField')()),
            ('expire', self.gf('django.db.models.fields.DateTimeField')()),
            ('price', self.gf('currencyfield.fields.CurrencyField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('ttrade', ['Listing'])

        # Adding M2M table for field offers on 'Listing'
        db.create_table('ttrade_listing_offers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('listing', models.ForeignKey(orm['ttrade.listing'], null=False)),
            ('offer', models.ForeignKey(orm['ttrade.offer'], null=False))
        ))
        db.create_unique('ttrade_listing_offers', ['listing_id', 'offer_id'])

        # Adding model 'Offer'
        db.create_table('ttrade_offer', (
            ('offerID', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Offerer', to=orm['auth.User'])),
            ('price', self.gf('currencyfield.fields.CurrencyField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('additional', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ttrade', ['Offer'])


    def backwards(self, orm):
        
        # Deleting model 'Listing'
        db.delete_table('ttrade_listing')

        # Removing M2M table for field offers on 'Listing'
        db.delete_table('ttrade_listing_offers')

        # Deleting model 'Offer'
        db.delete_table('ttrade_offer')


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
        'ttrade.listing': {
            'Meta': {'object_name': 'Listing'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expire': ('django.db.models.fields.DateTimeField', [], {}),
            'listingID': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listingType': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'offers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['ttrade.Offer']", 'null': 'True', 'blank': 'True'}),
            'picture': ('stdimage.fields.StdImageField', [], {'blank': 'True', 'max_length': '100', 'upload_to': "'ttrade/images/upload/'", 'size': "{'width': 560, 'force': None, 'height': 800}"}),
            'posted': ('django.db.models.fields.DateTimeField', [], {}),
            'price': ('currencyfield.fields.CurrencyField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Lister'", 'to': "orm['auth.User']"})
        },
        'ttrade.offer': {
            'Meta': {'object_name': 'Offer'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'additional': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'offerID': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('currencyfield.fields.CurrencyField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Offerer'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['ttrade']
