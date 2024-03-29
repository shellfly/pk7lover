# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Gallery'
        db.create_table('albums_gallery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('perm', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('comment', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('photo_num', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('cover', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('albums', ['Gallery'])

        # Adding model 'Photo'
        db.create_table('albums_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['albums.Gallery'])),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=225)),
            ('thumb128', self.gf('django.db.models.fields.CharField')(max_length=225)),
            ('thumb64', self.gf('django.db.models.fields.CharField')(max_length=225)),
            ('square', self.gf('django.db.models.fields.CharField')(max_length=225)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=225)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('stars', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('albums', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Gallery'
        db.delete_table('albums_gallery')

        # Deleting model 'Photo'
        db.delete_table('albums_photo')


    models = {
        'albums.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'comment': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cover': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'perm': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'photo_num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'albums.photo': {
            'Meta': {'object_name': 'Photo'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '225'}),
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['albums.Gallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '225'}),
            'square': ('django.db.models.fields.CharField', [], {'max_length': '225'}),
            'stars': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'thumb128': ('django.db.models.fields.CharField', [], {'max_length': '225'}),
            'thumb64': ('django.db.models.fields.CharField', [], {'max_length': '225'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
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
        }
    }

    complete_apps = ['albums']