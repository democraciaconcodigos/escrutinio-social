import re
from django import forms
from django.forms.models import modelform_factory
from django.forms import modelformset_factory, BaseModelFormSet
from django.utils.safestring import mark_safe
from material import Layout, Row, Fieldset
from .models import Voluntario, DatoDeContacto, VotoMesaReportado
from elecciones.models import Mesa, Eleccion, LugarVotacion, Circuito, Seccion
from localflavor.ar.forms import ARDNIField
from django.core.validators import validate_email, URLValidator
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.forms import generic_inlineformset_factory
import phonenumbers


OPCION_CANTIDAD_DE_SOBRES = 22
OPCION_HAN_VOTADO = 21
OPCION_DIFERENCIA = 23
OPCION_TOTAL_VOTOS = 20

LINK = 'Si tenés dudas consultá el <a href="https://www.padron.gob.ar" target="_blank">padrón</a>'


CARACTERISTICA_DEFAULT = '11'  # Buenos Aires

USERNAME_PATTERNS = {
    'twitter': re.compile(r'^((?:https?://(www\.)?twitter\.com/)|@)?(?P<username>\w{1,15})/?$'),
    'instagram': re.compile(r'^((?:https?://(www\.)?instagram\.com/)|@)?(?P<username>\w{3,20})/?$'),
    'facebook': re.compile(r'^(?:https?://(www\.)?facebook\.com/)?/?(?P<username>[\w\.]{3,50})/?(\?.*)?$'),
    'youtube': re.compile(r'^(?:https?://(www\.)?youtube\.com/(user/)?)?(?P<username>\w{3,40})/?$')
}


def validar_telefono(valor):
    valor = valor.strip()
    if valor.startswith(('15', '4')):
        valor = f'{CARACTERISTICA_DEFAULT} {valor}'
    elif valor.startswith('11') and 9 <= len(valor) <= 11:
        valor = f'9 {valor}'
    valor = phonenumbers.parse(valor, 'AR')
    formato = phonenumbers.PhoneNumberFormat.INTERNATIONAL
    valor = phonenumbers.format_number(valor, formato)
    return valor


class DatoDeContactoModelForm(forms.ModelForm):
    class Meta:
        model = DatoDeContacto
        exclude = []

    def clean_email(self, valor):
        try:
            validate_email(valor)
        except forms.ValidationError:
            self.add_error('valor', 'No es un email válido')

    def clean_telefono(self, valor):
        try:
            valor = validar_telefono(valor)
        except (AttributeError, phonenumbers.NumberParseException):
            self.add_error('valor', 'No es un teléfono válido')

        return valor

    def clean_username(self, tipo, valor):
        try:
            return re.match(USERNAME_PATTERNS[tipo], valor).group('username')
        except AttributeError:
            self.add_error('valor', f'No es un nombre de usuario de {tipo} válido')

    def clean_url(self, valor):
        validator = URLValidator()
        try:
            validator(valor)
        except ValidationError:
            self.add_error('valor', 'No es una dirección web válida')

    def clean(self):
        tipo = self.cleaned_data.get("tipo")
        valor = self.cleaned_data.get("valor", '').strip()

        if tipo == 'email':
            self.clean_email(valor)
        elif tipo == 'teléfono':
            valor = self.clean_telefono(valor)
        elif tipo in USERNAME_PATTERNS:
            valor = self.clean_username(tipo, valor)
        elif tipo == 'web':
            self.clean_url(valor)

        self.cleaned_data['valor'] = valor




class AuthenticationFormCustomError(AuthenticationForm):

    error_messages = {
        'invalid_login': "Por favor introducí un nombre de usuario y una contraseña correctos. Probá tu DNI sin puntos.",
        'inactive': _("This account is inactive."),
    }



def opciones_actuales():
    try:
        return Eleccion.opciones_actuales().count()
    except:
        return 0


class VoluntarioForm(forms.ModelForm):

    dni = ARDNIField(required=False)

    class Meta:
        model = Voluntario
        exclude = []


class MisDatosForm(VoluntarioForm):
    class Meta:
        model = Voluntario
        fields = [
            'nombre', 'apellido',
            'tipo_dni', 'dni',
        ]


class VoluntarioFormSimple(VoluntarioForm):

    class Meta:
        model = Voluntario
        fields = [
            'nombre', 'apellido',
            'dni',
        ]



class VoluntarioForm(forms.ModelForm):

    dni = ARDNIField(required=False)

    class Meta:
        model = Voluntario
        exclude = []


class QuieroSerVoluntario1(forms.Form):
    dni = ARDNIField(required=True, help_text='Ingresá tu Nº de documento')
    email = forms.EmailField(required=True)
    email2 = forms.EmailField(required=True, label="Confirmar email")

    layout = Layout('dni',
                    Row('email', 'email2'))


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email2 = cleaned_data.get('email2')
        if email and email2 and email != email2:
            self.add_error('email', 'Los emails no coinciden')
            self.add_error('email2', 'Los emails no coinciden')


class QuieroSerVoluntario2(forms.ModelForm):
    nombre = forms.CharField()
    apellido = forms.CharField()
    telefono = forms.CharField(label='Teléfono', help_text='Preferentemente celular')
    movilidad = forms.BooleanField(
        label='¿Tenés Movilidad propia?', required=False,
        help_text='Marcá la casilla si tenés cómo movilizarte el día de la elección'
    )
    seccion = forms.ModelChoiceField(label='Sección electoral', queryset=Seccion.objects.all(),
        help_text=mark_safe(f'Sección/departamento donde votás y/o fiscalizás. {LINK}')
    )

    layout = Layout(Row('nombre', 'apellido'),
                    'telefono',
                    Row('movilidad', 'disponibilidad'),
                    Fieldset('¿Dónde votás?',
                             'seccion'))
    class Meta:
        model = Voluntario
        fields = ['nombre', 'apellido', 'telefono', 'seccion']


    def clean_telefono(self):
        valor = self.cleaned_data['telefono']
        try:
            valor = validar_telefono(valor)
        except (AttributeError, phonenumbers.NumberParseException):
            raise forms.ValidationError('No es un teléfono válido')
        return valor


class QuieroSerVoluntario3(forms.Form):
    circuito = forms.ModelChoiceField(queryset=Circuito.objects.all(),
        help_text=mark_safe(f'Circuito/zona donde votás y/o fiscalizás. {LINK}')
    )


class QuieroSerVoluntario4(forms.Form):
    escuela = forms.ModelChoiceField(queryset=LugarVotacion.objects.all(),
        help_text=mark_safe(f'Escuela donde votás y/o fiscalizás. {LINK}')
    )


class VotoMesaModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['opcion'].label = ''
        self.fields['votos'].label = ''
        self.fields['votos'].required = False

        # self.fields['opcion'].widget.attrs['disabled'] = 'disabled'

    # layout = Layout(Row('opcion', 'votos'))

    class Meta:
        model = VotoMesaReportado
        fields = ('opcion', 'votos')


class BaseVotoMesaReportadoFormSet(BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.warnings = []

    """
    def clean(self):
        super().clean()
        diferencia = 0
        total_en_acta = 0
        cantidad_sobres = 0
        han_votado = 0

        suma = 0
        for form in self.forms:
            opcion = form.cleaned_data['opcion']
            if opcion.id == OPCION_CANTIDAD_DE_SOBRES:
                cantidad_sobres = form.cleaned_data.get('votos') or 0
            elif opcion.id == OPCION_HAN_VOTADO:
                han_votado = form.cleaned_data.get('votos') or 0
            elif opcion.id == OPCION_DIFERENCIA:
                diferencia = form.cleaned_data.get('votos') or 0
                form_opcion_dif = form
            elif opcion.id == OPCION_TOTAL_VOTOS:
                form_opcion_total = form
                total_en_acta = form.cleaned_data.get('votos') or 0
            else:
                suma += form.cleaned_data.get('votos') or 0

        if abs(diferencia) != abs(cantidad_sobres - han_votado):

            # form_opcion_dif.add_error('votos', 'Diferencia no válida')
            self.warnings.append((form_opcion_dif, 'votos', 'Diferencia no valida'))

        if suma != total_en_acta:
            #form_opcion_total.add_error(
            #    'votos', 'La sumatoria no se corresponde con el total'
            #)
            self.warnings.append((form_opcion_total, 'votos', 'La sumatoria no se corresponde con el total'))

        if cantidad_sobres != total_en_acta:
            # form_opcion_total.add_error(
            #    'votos', 'El total no corresponde a la cantidad de sobres'
            # )
            self.warnings.append((form_opcion_total, 'votos', 'El total no corresponde a la cantidad de sobres'))
        """

VotoMesaReportadoFormset = modelformset_factory(
    VotoMesaReportado, form=VotoMesaModelForm,
    formset=BaseVotoMesaReportadoFormSet,
    min_num=opciones_actuales(), extra=0, can_delete=False
)


ContactoInlineFormset = generic_inlineformset_factory(DatoDeContacto, form=DatoDeContactoModelForm, can_delete=True)

ActaMesaModelForm = modelform_factory(
    Mesa,
    fields=['foto_acta'],
)
