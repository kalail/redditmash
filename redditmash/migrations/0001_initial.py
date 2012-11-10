# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Post'
        db.create_table('redditmash_post', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_on_reddit', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('redditmash', ['Post'])

        # Adding model 'StatsReddit'
        db.create_table('redditmash_statsreddit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['redditmash.Post'], unique=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
            ('edited_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('redditmash', ['StatsReddit'])

        # Adding model 'Stats'
        db.create_table('redditmash_stats', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['redditmash.Post'], unique=True)),
            ('rating', self.gf('django.db.models.fields.FloatField')()),
            ('rank', self.gf('django.db.models.fields.IntegerField')()),
            ('edited_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('redditmash', ['Stats'])


    def backwards(self, orm):
        # Deleting model 'Post'
        db.delete_table('redditmash_post')

        # Deleting model 'StatsReddit'
        db.delete_table('redditmash_statsreddit')

        # Deleting model 'Stats'
        db.delete_table('redditmash_stats')


    models = {
        'redditmash.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.TextField', [], {}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_on_reddit': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
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