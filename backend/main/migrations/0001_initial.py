# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Archive'
        db.create_table(u'main_archive', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'main', ['Archive'])

        # Adding model 'Title'
        db.create_table(u'main_title', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('archive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Archive'])),
        ))
        db.send_create_signal(u'main', ['Title'])

        # Adding model 'Volume'
        db.create_table(u'main_volume', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Title'])),
        ))
        db.send_create_signal(u'main', ['Volume'])

        # Adding model 'Section'
        db.create_table(u'main_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('volume', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Volume'])),
        ))
        db.send_create_signal(u'main', ['Section'])

        # Adding model 'Article'
        db.create_table(u'main_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Section'])),
        ))
        db.send_create_signal(u'main', ['Article'])

        # Adding model 'Page'
        db.create_table(u'main_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Section'])),
        ))
        db.send_create_signal(u'main', ['Page'])

        # Adding M2M table for field articles on 'Page'
        m2m_table_name = db.shorten_name(u'main_page_articles')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm[u'main.page'], null=False)),
            ('article', models.ForeignKey(orm[u'main.article'], null=False))
        ))
        db.create_unique(m2m_table_name, ['page_id', 'article_id'])

        # Adding model 'Paragraph'
        db.create_table(u'main_paragraph', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Article'])),
        ))
        db.send_create_signal(u'main', ['Paragraph'])


    def backwards(self, orm):
        # Deleting model 'Archive'
        db.delete_table(u'main_archive')

        # Deleting model 'Title'
        db.delete_table(u'main_title')

        # Deleting model 'Volume'
        db.delete_table(u'main_volume')

        # Deleting model 'Section'
        db.delete_table(u'main_section')

        # Deleting model 'Article'
        db.delete_table(u'main_article')

        # Deleting model 'Page'
        db.delete_table(u'main_page')

        # Removing M2M table for field articles on 'Page'
        db.delete_table(db.shorten_name(u'main_page_articles'))

        # Deleting model 'Paragraph'
        db.delete_table(u'main_paragraph')


    models = {
        u'main.archive': {
            'Meta': {'object_name': 'Archive'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.article': {
            'Meta': {'object_name': 'Article'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Section']"})
        },
        u'main.page': {
            'Meta': {'object_name': 'Page'},
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pages'", 'symmetrical': 'False', 'to': u"orm['main.Article']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Section']"})
        },
        u'main.paragraph': {
            'Meta': {'object_name': 'Paragraph'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Article']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.section': {
            'Meta': {'object_name': 'Section'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'volume': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Volume']"})
        },
        u'main.title': {
            'Meta': {'object_name': 'Title'},
            'archive': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Archive']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.volume': {
            'Meta': {'object_name': 'Volume'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Title']"})
        }
    }

    complete_apps = ['main']