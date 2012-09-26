# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PhotoSaying'
        db.delete_table('broadcast_photosaying')

        # Deleting model 'PartSaying'
        db.delete_table('broadcast_partsaying')

        # Deleting model 'ActivitySaying'
        db.delete_table('broadcast_activitysaying')


    def backwards(self, orm):
        # Adding model 'PhotoSaying'
        db.create_table('broadcast_photosaying', (
            ('num', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['albums.Gallery'])),
        ))
        db.send_create_signal('broadcast', ['PhotoSaying'])

        # Adding model 'PartSaying'
        db.create_table('broadcast_partsaying', (
            ('photo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.Photograph'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.Activity'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('broadcast', ['PartSaying'])

        # Adding model 'ActivitySaying'
        db.create_table('broadcast_activitysaying', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.Activity'])),
        ))
        db.send_create_signal('broadcast', ['ActivitySaying'])


    models = {
        
    }

    complete_apps = ['broadcast']