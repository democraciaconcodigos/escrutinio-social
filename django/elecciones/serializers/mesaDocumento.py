from rest_framework import serializers
from elecciones.models import MesaDocumento

class MesaDocumentoSerializers(serializers.ModelSerializer):
    class Meta:
        model = MesaDocumento
        fields = '__all__'
