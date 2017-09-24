import re
import uuid
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from elecciones.models import desde_hasta, Mesa, LugarVotacion

from model_utils.fields import StatusField
from model_utils import Choices



class DatoDeContacto(models.Model):
    """Modelo generérico para guardar datos de contacto de personas o medios"""

    TIPOS = Choices(
        'teléfono', 'email', 'web', 'twitter', 'facebook',
        'instagram', 'youtube', 'skype'
    )

    tipo = models.CharField(choices=TIPOS, max_length=20)
    valor = models.CharField(max_length=100)
    # generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (('tipo', 'valor', 'content_type', 'object_id'),)


    def __str__(self):
        return f'{self.tipo}: {self.valor}'


class Voluntario(models.Model):
    TIPO_DNI = Choices('DNI', 'CI', 'LE', 'LC')
    ESTADOS = Choices('PRE-INSCRIPTO', 'CONFIRMADO', 'DECLINADO')
    estado = StatusField(choices_name='ESTADOS', default='PRE-INSCRIPTO')

    escuela_donde_vota = models.ForeignKey('elecciones.LugarVotacion', null=True, blank=True)

    codigo_confirmacion = models.UUIDField(default=uuid.uuid4, editable=False)
    email_confirmado = models.BooleanField(default=False)

    apellido = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)

    tipo_dni = models.CharField(choices=TIPO_DNI, max_length=3, default='DNI')
    dni = models.CharField(max_length=15, blank=True, null=True)

    datos_de_contacto = GenericRelation('DatoDeContacto', related_query_name='voluntarios')

    user = models.OneToOneField('auth.User', null=True,
                    blank=True, related_name='voluntario',
                    on_delete=models.SET_NULL)


    class Meta:
        verbose_name_plural = 'Voluntari@s'
        unique_together = (('tipo_dni', 'dni'),)

    def agregar_dato_de_contacto(self, tipo, valor):
        type_ = ContentType.objects.get_for_model(self)
        try:
            DatoDeContacto.objects.get(content_type__pk=type_.id, object_id=self.id, tipo=tipo, valor=valor)
        except DatoDeContacto.DoesNotExist:
            DatoDeContacto.objects.create(content_object=self, tipo=tipo, valor=valor)

    @property
    def telefonos(self):
        return self.datos_de_contacto.filter(tipo='teléfono').values_list('valor', flat=True)

    @property
    def emails(self):
        return self.datos_de_contacto.filter(tipo='email').values_list('valor', flat=True)


    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    @property
    def asignaciones_pendientes(self):
        ids = VotoMesaReportado.objects.filter(voluntario=self).distinct('mesa__id').values_list('mesa__id', flat=True)
        return self.asignaciones.exclude(mesa__id__in=ids)


class AsignacionVoluntario(TimeStampedModel):

    mesa = models.ForeignKey('elecciones.Mesa', related_name='voluntarios')
    voluntario = models.ForeignKey('Voluntario', related_name='asignaciones')

    def get_absolute_url(self):
        return reverse('cargar', args=(self.id,))


    def __str__(self):
        return f'Asignacion {self.mesa}: {self.voluntario}'

    class Meta:
        verbose_name = 'Asignación de voluntari@'
        verbose_name_plural = 'Asignación de voluntari@s'



@receiver(post_save, sender=Voluntario)
def crear_user_para_voluntario(sender, instance=None, created=False, **kwargs):
    if not instance.user and instance.dni and instance.estado == 'CONFIRMADO':
        user = User(
            username=re.sub("[^0-9]", "", instance.dni),
            first_name=instance.nombre,
            last_name=instance.apellido,
            is_active=True,
        )

        user.set_password(settings.DEFAULT_PASS_PREFIX + instance.dni[-3:])
        user.save()
        instance.user = user
        instance.save(update_fields=['user'])


@receiver(pre_delete, sender=Voluntario)
def borrar_user_para_fiscal(sender, instance=None, **kwargs):
    if instance.user:
        instance.user.delete()



class AbstractVotoMesa(models.Model):
    mesa = models.ForeignKey('elecciones.Mesa')
    opcion = models.ForeignKey('elecciones.Opcion')
    votos = models.PositiveIntegerField(null=True)

    class Meta:
        abstract = True
        unique_together = ('mesa', 'opcion')


    def __str__(self):
        return f"{self.mesa} - {self.opcion}: {self.votos}"


class VotoMesaReportado(AbstractVotoMesa):
    voluntario = models.ForeignKey('fiscales.Voluntario')



class VotoMesaOficial(AbstractVotoMesa):
    pass
