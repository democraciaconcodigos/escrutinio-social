from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.utils.safestring import mark_safe
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView

from django.views.generic.base import ContextMixin
from annoying.functions import get_object_or_None
from .models import Voluntario, AsignacionVoluntario, VotoMesaReportado
from elecciones.models import (
    Mesa, Eleccion, Circuito, LugarVotacion
)
from formtools.wizard.views import SessionWizardView
from django.template.loader import render_to_string
from html2text import html2text
from django.core.mail import send_mail

from .forms import (
    ContactoInlineFormset,
    MisDatosForm,
    VotoMesaReportadoFormset,
    ActaMesaModelForm,
    QuieroSerVoluntario1,
    QuieroSerVoluntario2,
    QuieroSerVoluntario3,
    QuieroSerVoluntario4,
)





def choice_home(request):
    """
    redirige a una página en funcion del tipo de usuario
    """

    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    try:
        user.voluntario
        return redirect('inicio')
    except Voluntario.DoesNotExist:
        if user.groups.filter(name='prensa').exists():
            return redirect('/prensa/')
        elif user.is_staff:
            return redirect('/admin/')


class ConContactosMixin(ContextMixin):
    inline_formset_class = ContactoInlineFormset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.POST:
            formset = self.inline_formset_class(self.request.POST, instance=self.object)
        else:
            formset = self.inline_formset_class(instance=self.object)
        context['formsets'] = {'Datos de contacto': formset}
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        valid = all(formset.is_valid() for formset in context['formsets'].values())
        if valid:
            self.object = form.save()
            for formset in context['formsets'].values():
                formset.instance = self.object
                formset.save()
            # ok, redirect
            return super().form_valid(form)

        # invalid formset
        return self.render_to_response(self.get_context_data(form=form))



class BaseVoluntario(LoginRequiredMixin, DetailView):
    model = Voluntario

    def get_object(self, *args, **kwargs):
        try:
            return self.request.user.voluntario
        except Voluntario.DoesNotExist:
            raise Http404('no está registrado como voluntario')


class QuieroSerVoluntario(SessionWizardView):
    form_list = [
        QuieroSerVoluntario1,
        QuieroSerVoluntario2,
        QuieroSerVoluntario3,
        QuieroSerVoluntario4
    ]

    def get_form_initial(self, step):
        if step != '0':
            dni = self.get_cleaned_data_for_step('0')['dni']
            email = self.get_cleaned_data_for_step('0')['email']
            fiscal = (get_object_or_None(Voluntario, dni=dni) or
                      get_object_or_None(Voluntario,
                                         datos_de_contacto__valor=email,
                                         datos_de_contacto__tipo='email'))

        if step == '1' and fiscal:
            if self.steps.current == '0':
                # sólo si acaba de llegar al paso '1' muestro mensaje
                messages.info(self.request, 'Ya estás en el sistema. Por favor, confirmá tus datos.')
            return {
                'nombre': fiscal.nombre,
                'apellido': fiscal.apellido,
                'telefono': fiscal.telefonos[0] if fiscal.telefonos else '',
                'seccion': fiscal.escuelas[0].circuito.seccion if fiscal.escuelas else None

            }
        elif step == '2' and fiscal:
            seccion = self.get_cleaned_data_for_step('1')['seccion']
            seccion_original = fiscal.escuelas[0].circuito.seccion if fiscal.escuelas else None

            if seccion_original and seccion == seccion_original:
                circuito = fiscal.escuelas[0].circuito
            else:
                circuito = None

            return {
                'circuito': circuito
            }
        elif step == '3' and fiscal:
            circuito = self.get_cleaned_data_for_step('2')['circuito']
            circuito_original = fiscal.escuelas[0].circuito if fiscal.escuelas else None

            if circuito_original and circuito == circuito_original:
                escuela = fiscal.escuelas[0]
            else:
                escuela = None

            return {
                'escuela': escuela
            }

        return self.initial_dict.get(step, {})

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)

        # determine the step if not given
        if step is None:
            step = self.steps.current

        if step == '2':
            seccion = self.get_cleaned_data_for_step('1')['seccion']
            form.fields['circuito'].queryset = Circuito.objects.filter(seccion=seccion)
        elif step == '3':
            circuito = self.get_cleaned_data_for_step('2')['circuito']
            form.fields['escuela'].queryset = LugarVotacion.objects.filter(circuito=circuito)
        return form

    def done(self, form_list, **kwargs):
        data = self.get_all_cleaned_data()
        dni = data['dni']
        email = data['email']
        fiscal = (get_object_or_None(Voluntario, dni=dni) or
                  get_object_or_None(Voluntario,
                                     datos_de_contacto__valor=email,
                                     datos_de_contacto__tipo='email'))
        if fiscal:
            fiscal.estado = 'AUTOCONFIRMADO'
        else:
            fiscal = Voluntario(estado='PRE-INSCRIPTO', tipo='de_mesa', dni=dni)

        fiscal.dni = dni
        fiscal.nombre = data['nombre']
        fiscal.apellido = data['apellido']
        fiscal.escuela_donde_vota = data['escuela']
        fiscal.save()
        fiscal.agregar_dato_de_contacto('teléfono', data['telefono'])
        fiscal.agregar_dato_de_contacto('email', email)

        body_html = render_to_string('fiscales/email.html', {'fiscal': fiscal,})
        body_text = html2text(body_html)

        send_mail(
            'Recibimos tu inscripción como voluntario',
            body_text,
            'info@cordobaciudadana.org',
            [email],
            fail_silently=False,
            html_message=body_html
        )

        return render(self.request, 'formtools/wizard/wizard_done.html', {
            'fiscal': fiscal,
        })


def confirmar_email(request, uuid):
    fiscal = get_object_or_None(Voluntario, codigo_confirmacion=uuid)
    if not fiscal:
        texto = mark_safe('El código de confirmación es inválido. '
                          'Por favor copiá y pegá el link que te enviamos'
                          ' por email en la barra de direcciones'
                          'Si seguís con problemas, env '
                          '<a href="mailto:fiscales@cordobaciudadana.org">'
                          'fiscales@cordobaciudadana.org</a>')

    elif fiscal.email_confirmado:
        texto = 'Tu email ya estaba confirmado. Gracias.'
    else:
        fiscal.email_confirmado = True
        fiscal.save(update_fields=['email_confirmado'])
        texto = 'Confirmamos tu email exitosamente. ¡Gracias!'

    return render(
        request, 'fiscales/confirmar_email.html',
        {'texto': texto, 'fiscal': fiscal}
    )




def email(request):
    html = render_to_string('fiscales/email.html', {'nombre': 'Pedro'})
    return HttpResponse(html2text(html), content_type='plain/text')
    # return render(request, 'fiscales/email.html', {})


class MisDatos(BaseVoluntario):
    template_name = "fiscales/mis-datos.html"


class MisDatosUpdate(ConContactosMixin, UpdateView, BaseVoluntario):
    """muestras los contactos para un fiscal"""
    form_class = MisDatosForm
    template_name = "fiscales/mis-datos-update.html"

    def get_success_url(self):
        return reverse('mis-datos')



class MesaActa(BaseVoluntario, UpdateView):
    template_name = "fiscales/cargar-foto.html"
    slug_field = 'numero'
    slug_url_kwarg = 'mesa_numero'
    model = Mesa
    form_class = ActaMesaModelForm

    def get_object(self):
        return get_object_or_404(Mesa,
                                 numero=self.kwargs['mesa_numero'], estado='ESCRUTADA')

    def form_valid(self, form):
        super().form_valid(form)
        messages.success(self.request, 'Foto subida correctamente ¡Gracias!')
        return redirect(self.object.get_absolute_url())


class Inicio(BaseVoluntario):
    template_name = "fiscales/inicio.html"


@login_required
def cargar_resultados(request, asignacion_id):
    def fix_opciones(formset):
        # hack para dejar sólo la opcion correspondiente a cada fila
        # se podria hacer "disabled" pero ese caso quita el valor del
        # cleaned_data y luego lo exige por ser requerido.
        for i, (opcion, form) in enumerate(zip(Eleccion.opciones_actuales(), formset), 1):
            form.fields['opcion'].choices = [(opcion.id, str(opcion))]
            form.fields['opcion'].widget.attrs['tabindex'] = 99 + i

            form.fields['votos'].required = True
            form.fields['votos'].widget.attrs['tabindex'] = i
            if i == 1:
                form.fields['votos'].widget.attrs['autofocus'] = True

    asignacion = get_object_or_404(AsignacionVoluntario,
        id=asignacion_id, voluntario=request.user.voluntario
    )
    mesa, voluntario = asignacion.mesa, asignacion.voluntario
    data = request.POST if request.method == 'POST' else None
    qs = VotoMesaReportado.objects.filter(mesa=mesa, voluntario=voluntario)
    initial = [{'opcion': o} for o in Eleccion.opciones_actuales()]
    formset = VotoMesaReportadoFormset(data, queryset=qs, initial=initial)

    fix_opciones(formset)

    is_valid = False
    if qs:
        formset.convert_warnings = True  # monkepatch

    if request.method == 'POST' or qs:
        is_valid = formset.is_valid()

    # = Eleccion.objects.last()
    if is_valid:
        for form in formset:
            vmr = form.save(commit=False)
            vmr.mesa = mesa
            vmr.voluntario = voluntario
            vmr.save()

        if formset.warnings:
            messages.warning(request, 'Guardado con inconsistencias')
        else:
            messages.success(request, 'Guardado correctamente')

        return redirect('inicio')

    return render(request, "fiscales/carga.html",
                  {'formset': formset, 'object': mesa})


class CambiarPassword(PasswordChangeView):
    template_name = "fiscales/cambiar-contraseña.html"
    success_url = reverse_lazy('mis-datos')

    def form_valid(self, form):
        messages.success(self.request, 'Tu contraseña se cambió correctamente')
        return super().form_valid(form)


