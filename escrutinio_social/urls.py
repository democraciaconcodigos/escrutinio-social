from django.conf.urls import url, include
from django.contrib import admin
from material.frontend import urls as frontend_urls
from elecciones import urls as elecciones_urls
from fiscales import urls as fiscales_urls
from fiscales.views import choice_home, QuieroSerVoluntario, email, confirmar_email
from fiscales.forms import AuthenticationFormCustomError
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^$', choice_home, name="home"),
    url(r'^_email/$', email),
    url(r'^quiero-ser-voluntario/$', QuieroSerVoluntario.as_view(), name='quiero-ser-fiscal'),
    url(r'^quiero-ser-voluntario/confirmar-email/(?P<uuid>[0-9a-f-]+)$', confirmar_email, name='confirmar-email'),
    url(r'^login/$', auth_views.LoginView.as_view(authentication_form=AuthenticationFormCustomError)),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(authentication_form=AuthenticationFormCustomError)),


    url(r'', include(frontend_urls)),
    url(r'', include('django.contrib.auth.urls')),
    url(r'', include(fiscales_urls)),
    url(r'^hijack/', include('hijack.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^elecciones/', include(elecciones_urls)),
]
