# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ExampleModel'
        db.create_table('example_cms_app_examplemodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('example_cms_app', ['ExampleModel'])

        # Adding model 'AnotherExampleModel'
        db.create_table('example_cms_app_anotherexamplemodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128, db_index=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('long_field', self.gf('django.db.models.fields.TextField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('example_cms_app', ['AnotherExampleModel'])

        # Adding M2M table for field region on 'AnotherExampleModel'
        db.create_table('example_cms_app_anotherexamplemodel_region', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('anotherexamplemodel', models.ForeignKey(orm['example_cms_app.anotherexamplemodel'], null=False)),
            ('examplemodel', models.ForeignKey(orm['example_cms_app.examplemodel'], null=False))
        ))
        db.create_unique('example_cms_app_anotherexamplemodel_region', ['anotherexamplemodel_id', 'examplemodel_id'])


    def backwards(self, orm):
        
        # Deleting model 'ExampleModel'
        db.delete_table('example_cms_app_examplemodel')

        # Deleting model 'AnotherExampleModel'
        db.delete_table('example_cms_app_anotherexamplemodel')

        # Removing M2M table for field region on 'AnotherExampleModel'
        db.delete_table('example_cms_app_anotherexamplemodel_region')


    models = {
        'example_cms_app.anotherexamplemodel': {
            'Meta': {'object_name': 'AnotherExampleModel'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'long_field': ('django.db.models.fields.TextField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['example_cms_app.ExampleModel']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'example_cms_app.examplemodel': {
            'Meta': {'object_name': 'ExampleModel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['example_cms_app']
