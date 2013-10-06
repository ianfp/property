# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Task'
        db.create_table('tasks_task', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('_frequency', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='frequency')),
            ('priority', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('tasks', ['Task'])

        # Adding model 'Contact'
        db.create_table('tasks_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
        ))
        db.send_create_signal('tasks', ['Contact'])

        # Adding model 'Supplier'
        db.create_table('tasks_supplier', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
        ))
        db.send_create_signal('tasks', ['Supplier'])

        # Adding M2M table for field contacts on 'Supplier'
        m2m_table_name = db.shorten_name('tasks_supplier_contacts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('supplier', models.ForeignKey(orm['tasks.supplier'], null=False)),
            ('contact', models.ForeignKey(orm['tasks.contact'], null=False))
        ))
        db.create_unique(m2m_table_name, ['supplier_id', 'contact_id'])

        # Adding model 'Estimate'
        db.create_table('tasks_estimate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('supplier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tasks.Supplier'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('tasks', ['Estimate'])

        # Adding M2M table for field tasks on 'Estimate'
        m2m_table_name = db.shorten_name('tasks_estimate_tasks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('estimate', models.ForeignKey(orm['tasks.estimate'], null=False)),
            ('task', models.ForeignKey(orm['tasks.task'], null=False))
        ))
        db.create_unique(m2m_table_name, ['estimate_id', 'task_id'])


    def backwards(self, orm):
        # Deleting model 'Task'
        db.delete_table('tasks_task')

        # Deleting model 'Contact'
        db.delete_table('tasks_contact')

        # Deleting model 'Supplier'
        db.delete_table('tasks_supplier')

        # Removing M2M table for field contacts on 'Supplier'
        db.delete_table(db.shorten_name('tasks_supplier_contacts'))

        # Deleting model 'Estimate'
        db.delete_table('tasks_estimate')

        # Removing M2M table for field tasks on 'Estimate'
        db.delete_table(db.shorten_name('tasks_estimate_tasks'))


    models = {
        'tasks.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'})
        },
        'tasks.estimate': {
            'Meta': {'object_name': 'Estimate'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Supplier']"}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tasks.Task']", 'symmetrical': 'False'})
        },
        'tasks.supplier': {
            'Meta': {'object_name': 'Supplier'},
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tasks.Contact']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'tasks.task': {
            'Meta': {'object_name': 'Task'},
            '_frequency': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'frequency'"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['tasks']