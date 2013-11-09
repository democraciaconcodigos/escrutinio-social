from tastypie.resources import ModelResource
from core.models import * 

class ProvinciaResource(ModelResource):
	class Meta:
		queryset = Provincia.objects.all()
		resource_name = 'provincia'

class MunicipioResource(ModelResource):
	class Meta:
		queryset = Municipio.objects.all()
		resource_name = 'municipio'

class CircuitoResource(ModelResource):
	class Meta:
		queryset = Circuito.objects.all()
		resource_name = 'circuito'

class LugarVotacionResource(ModelResource):
	class Meta:
		queryset = LugarVotacion.objects.all()
		resource_name = 'lugar_votacion'

class MesaResource(ModelResource):
	class Meta:
		queryset = Mesa.objects.all()
		resource_name = 'mesa'

class OpcionResource(ModelResource):
	class Meta:
		queryset = Opcion.objects.all()
		resource_name = 'opcion'

class EleccionResource(ModelResource):
	class Meta:
		queryset = Eleccion.objects.all()
		resource_name = 'eleccion'

class VotoMesaOficialResource(ModelResource):
	class Meta:
		queryset = VotoMesaOficial.objects.all()
		resource_name = 'voto_mesa_oficial'

class VotoMesaSocialResource(ModelResource):
	class Meta:
		queryset = VotoMesaSocial.objects.all()
		resource_name = 'voto_mesa_social'

class VotoMesaOCRResource(ModelResource):
	class Meta:
		queryset = VotoMesaOCR.objects.all()
		resource_name = 'voto_mesa_ocr'
