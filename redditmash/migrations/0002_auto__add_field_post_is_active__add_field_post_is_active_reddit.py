# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.is_active'
        db.add_column('redditmash_post', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Post.is_active_reddit'
        db.add_column('redditmash_post', 'is_active_reddit',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Post.is_active'
        db.delete_column('redditmash_post', 'is_active')

        # Deleting field 'Post.is_active_reddit'
        db.delete_column('redditmash_post', 'is_active_reddit')


    models = {
        'redditmash.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.TextField', [], {}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_on_reddit': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active_reddit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'redditmash.stats': {
            'Meta': {'object_name': 'Stats'},
            'edited_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['redditmash.Post']", 'unique': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'rating': ('django.db.models.fields.FloatField', [], {})
        },
        'redditmash.statsreddit': {
            'Meta': {'object_name': 'StatsReddit'},
            'edited_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['redditmash.Post']", 'unique': 'True'}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'score': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['redditmash']