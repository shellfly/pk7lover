# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Saying'
        db.delete_table('broadcast_saying')

        # Adding model 'PartSaying'
        db.create_table('broadcast_partsaying', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.Activity'])),
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.Photograph'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('broadcast', ['PartSaying'])


    def backwards(self, orm):
        # Adding model 'Saying'
        db.create_table('broadcast_saying', (
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 9, 25, 0, 0))),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('broadcast', ['Saying'])

        # Deleting model 'PartSaying'
        db.delete_table('broadcast_partsaying')


    models = {
        'activity.activity': {
            'Meta': {'object_name': 'Activity'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'beg_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'photo_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'subject': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'activity.photograph': {
            'Meta': {'object_name': 'Photograph'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Activity']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'join_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '225'}),
            'thumb128': ('django.db.models.fields.CharField', [], {'max_length': '225'}),
            'thumb64': ('django.db.models.fields.CharField', [], {'max_length': '225'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
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
        'broadcast.activitysaying': {
            'Meta': {'object_name': 'ActivitySaying'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'broadcast.partsaying': {
            'Meta': {'object_name': 'PartSaying'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Photograph']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'broadcast.photosaying': {
            'Meta': {'object_name': 'PhotoSaying'},
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['albums.Gallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['broadcast']