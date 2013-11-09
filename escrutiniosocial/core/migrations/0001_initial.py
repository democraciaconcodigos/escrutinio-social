# -*- coding: utf-8 -*-

from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Provincia'
        db.create_table(u'core_provincia', (
            ('dne_id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Provincia'])

        # Adding model 'Municipio'
        db.create_table(u'core_municipio', (
            ('dne_id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('provincia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Provincia'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Municipio'])

        # Adding model 'Circuito'
        db.create_table(u'core_circuito', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('municipio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Municipio'])),
            ('numero', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Circuito'])

        # Adding model 'LugarVotacion'
        db.create_table(u'core_lugarvotacion', (
            ('dne_id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('circuito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Circuito'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['LugarVotacion'])

        # Adding model 'Mesa'
        db.create_table(u'core_mesa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('circuito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Circuito'])),
            ('lugarvotacion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.LugarVotacion'], null=True)),
            ('numero', self.gf('django.db.models.fields.IntegerField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'core', ['Mesa'])

        # Adding model 'Opcion'
        db.create_table(u'core_opcion', (
            ('nombre', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('dne_id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
        ))
        db.send_create_signal(u'core', ['Opcion'])

        # Adding model 'Eleccion'
        db.create_table(u'core_eleccion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'core', ['Eleccion'])

        # Adding M2M table for field opciones on 'Eleccion'
        m2m_table_name = db.shorten_name(u'core_eleccion_opciones')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('eleccion', models.ForeignKey(orm[u'core.eleccion'], null=False)),
            ('opcion', models.ForeignKey(orm[u'core.opcion'], null=False))
        ))
        db.create_unique(m2m_table_name, ['eleccion_id', 'opcion_id'])

        # Adding model 'VotoMesaOficial'
        db.create_table(u'core_votomesaoficial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mesa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Mesa'])),
            ('opcion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Opcion'])),
            ('votos', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['VotoMesaOficial'])

        # Adding unique constraint on 'VotoMesaOficial', fields ['mesa', 'opcion']
        db.create_unique(u'core_votomesaoficial', ['mesa_id', 'opcion_id'])

        # Adding model 'VotoMesaSocial'
        db.create_table(u'core_votomesasocial', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mesa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Mesa'])),
            ('opcion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Opcion'])),
            ('votos', self.gf('django.db.models.fields.IntegerField')()),
            ('usuario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'core', ['VotoMesaSocial'])

        # Adding unique constraint on 'VotoMesaSocial', fields ['mesa', 'opcion']
        db.create_unique(u'core_votomesasocial', ['mesa_id', 'opcion_id'])

        # Adding model 'VotoMesaOCR'
        db.create_table(u'core_votomesaocr', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mesa', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Mesa'])),
            ('opcion', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Opcion'])),
            ('votos', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['VotoMesaOCR'])

        # Adding unique constraint on 'VotoMesaOCR', fields ['mesa', 'opcion']
        db.create_unique(u'core_votomesaocr', ['mesa_id', 'opcion_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'VotoMesaOCR', fields ['mesa', 'opcion']
        db.delete_unique(u'core_votomesaocr', ['mesa_id', 'opcion_id'])

        # Removing unique constraint on 'VotoMesaSocial', fields ['mesa', 'opcion']
        db.delete_unique(u'core_votomesasocial', ['mesa_id', 'opcion_id'])

        # Removing unique constraint on 'VotoMesaOficial', fields ['mesa', 'opcion']
        db.delete_unique(u'core_votomesaoficial', ['mesa_id', 'opcion_id'])

        # Deleting model 'Provincia'
        db.delete_table(u'core_provincia')

        # Deleting model 'Municipio'
        db.delete_table(u'core_municipio')

        # Deleting model 'Circuito'
        db.delete_table(u'core_circuito')

        # Deleting model 'LugarVotacion'
        db.delete_table(u'core_lugarvotacion')

        # Deleting model 'Mesa'
        db.delete_table(u'core_mesa')

        # Deleting model 'Opcion'
        db.delete_table(u'core_opcion')

        # Deleting model 'Eleccion'
        db.delete_table(u'core_eleccion')

        # Removing M2M table for field opciones on 'Eleccion'
        db.delete_table(db.shorten_name(u'core_eleccion_opciones'))

        # Deleting model 'VotoMesaOficial'
        db.delete_table(u'core_votomesaoficial')

        # Deleting model 'VotoMesaSocial'
        db.delete_table(u'core_votomesasocial')

        # Deleting model 'VotoMesaOCR'
        db.delete_table(u'core_votomesaocr')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.circuito': {
            'Meta': {'object_name': 'Circuito'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'municipio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Municipio']"}),
            'numero': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.eleccion': {
            'Meta': {'object_name': 'Eleccion'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'opciones': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Opcion']", 'symmetrical': 'False'})
        },
        u'core.lugarvotacion': {
            'Meta': {'object_name': 'LugarVotacion'},
            'circuito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Circuito']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'dne_id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.mesa': {
            'Meta': {'object_name': 'Mesa'},
            'circuito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Circuito']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lugarvotacion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.LugarVotacion']", 'null': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'core.municipio': {
            'Meta': {'object_name': 'Municipio'},
            'dne_id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Provincia']"})
        },
        u'core.opcion': {
            'Meta': {'object_name': 'Opcion'},
            'dne_id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.provincia': {
            'Meta': {'object_name': 'Provincia'},
            'dne_id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.votomesaocr': {
            'Meta': {'unique_together': "(('mesa', 'opcion'),)", 'object_name': 'VotoMesaOCR'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mesa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Mesa']"}),
            'opcion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Opcion']"}),
            'votos': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.votomesaoficial': {
            'Meta': {'unique_together': "(('mesa', 'opcion'),)", 'object_name': 'VotoMesaOficial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mesa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Mesa']"}),
            'opcion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Opcion']"}),
            'votos': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.votomesasocial': {
            'Meta': {'unique_together': "(('mesa', 'opcion'),)", 'object_name': 'VotoMesaSocial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mesa': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Mesa']"}),
            'opcion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Opcion']"}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'votos': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['core']