from django.db.models import Q
from django.urls import reverse
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Voluntario, AsignacionVoluntario, DatoDeContacto
from .forms import VoluntarioForm, DatoDeContactoModelForm
from django_admin_row_actions import AdminRowActionsMixin
from django.contrib.admin.filters import DateFieldListFilter


class FechaIsNull(DateFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.links = self.links[-2:]


class ContactoAdminInline(GenericTabularInline):
    model = DatoDeContacto
    form = DatoDeContactoModelForm


class AsignadoFilter(admin.SimpleListFilter):
    title = 'Asignación'
    parameter_name = 'asignado'

    def lookups(self, request, model_admin):
        return (
            ('sí', 'sí'),
            ('no', 'no'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            isnull = value == 'no'
            general = Q(
                tipo='general',
                asignacion_escuela__isnull=isnull,
                asignacion_escuela__eleccion__slug='generales2017'
            )
            de_mesa = Q(
                tipo='de_mesa',
                asignacion_mesa__isnull=isnull,
                asignacion_mesa__mesa__eleccion__slug='generales2017'
            )
            queryset = queryset.filter(general | de_mesa)
        return queryset


class ReferenteFilter(admin.SimpleListFilter):
    title = 'Referente'
    parameter_name = 'referente'

    def lookups(self, request, model_admin):
        return (
            ('sí', 'sí'),
            ('no', 'no'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            isnull = value == 'no'
            queryset = queryset.filter(es_referente_de_circuito__isnull=isnull).distinct()
        return queryset



class VoluntarioAdmin(AdminRowActionsMixin, admin.ModelAdmin):

    def get_row_actions(self, obj):
        row_actions = []
        if obj.user:
            row_actions.append(
                {
                    'label': f'Loguearse como {obj.nombre}',
                    'url': f'/hijack/{obj.user.id}/',
                    'enabled': True,
                }
            )
        row_actions += super().get_row_actions(obj)
        return row_actions

    def telefonos(o):
        return ' / '.join(o.telefonos)


    form = VoluntarioForm
    list_display = ('__str__', 'dni', telefonos)
    search_fields = (
        'apellido', 'nombre', 'dni',
        'asignacion_escuela__lugar_votacion__nombre',
        'asignacion_mesa__mesa__lugar_votacion__nombre'
    )
    list_display_links = ('__str__',)
    list_filter = ('estado', 'email_confirmado', AsignadoFilter)
    # readonly_fields = ('mesas_desde_hasta',)
    inlines = [
        ContactoAdminInline,
    ]



class AsignacionVoluntarioAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    list_filter = ('mesa__eleccion', 'mesa__lugar_votacion__circuito')

    raw_id_fields = ("mesa", "voluntario")
    search_fields = (
        'voluntario__apellido', 'voluntario__nombre', 'voluntario__dni',
        'mesa__numero',
        'mesa__lugar_votacion__nombre',
        'mesa__lugar_votacion__direccion',
        'mesa__lugar_votacion__barrio',
        'mesa__lugar_votacion__ciudad',
    )


admin.site.register(AsignacionVoluntario, AsignacionVoluntarioAdmin)
admin.site.register(Voluntario, VoluntarioAdmin)

