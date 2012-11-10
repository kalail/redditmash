# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Choice'
        db.create_table('redditmash_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post_1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='post_1', to=orm['redditmash.Post'])),
            ('post_2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='post_2', to=orm['redditmash.Post'])),
            ('times_completed', self.gf('django.db.models.fields.IntegerField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('redditmash', ['Choice'])


    def backwards(self, orm):
        # Deleting model 'Choice'
        db.delete_table('redditmash_choice')


    models = {
        'redditmash.choice': {
            'Meta': {'object_name': 'Choice'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'post_1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_1'", 'to': "orm['redditmash.Post']"}),
            'post_2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_2'", 'to': "orm['redditmash.Post']"}),
            'times_completed': ('django.db.models.fields.IntegerField', [], {})
        },
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