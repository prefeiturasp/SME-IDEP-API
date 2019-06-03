"""indice_idep URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from escolas.api.viewsets import EscolasViewSet
from idep.views import MetasAnosFinais, MetasAnosIniciais, HistogramaIndicesIDEPAnoInicial, \
    HistogramaIndicesIDEPAnoFinal
from pessoas.views import LoginView, EscolasDoServidor
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='IDEP API')

router = routers.DefaultRouter()
router.register(r'escolas', EscolasViewSet)

urlpatterns = [path('', include(router.urls)),
               path(r'docs/', schema_view),
               path('admin/', admin.site.urls),
               path('login/', LoginView.as_view()),
               path('servidorescolas/<slug:rf>', EscolasDoServidor.as_view()),
               path('meta_ano_final/<slug:codesc>', MetasAnosFinais.as_view()),
               path('meta_ano_inicial/<slug:codesc>', MetasAnosIniciais.as_view()),
               path('indices_ano_inicial/<slug:codesc>', HistogramaIndicesIDEPAnoInicial.as_view()),
               path('indices_ano_final/<slug:codesc>', HistogramaIndicesIDEPAnoFinal.as_view()),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
