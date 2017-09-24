from rest_framework import serializers
from elecciones.models import Mesa

class MesaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = '__all__' 
