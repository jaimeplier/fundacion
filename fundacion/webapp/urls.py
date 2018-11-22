from django.urls import path

from adminstrador.views import AcudeInstitucionAdd, AcudeInstitucionAjaxList, AcudeInstitucionEdit, EstadoAdd, \
    EstadoAjaxList, EstadoEdit, PaisAdd, PaisAjaxList, PaisEdit, EstadoCivilAdd, EstadoCivilAjaxList, EstadoCivilEdit, \
    EstatusAdd, EstatusAjaxList, EstatusEdit, LenguaIndigenaAdd, LenguaIndigenaAjaxList, LenguaIndigenaEdit, \
    MedioContactoAdd, MedioContactoAjaxList, MedioContactoEdit, ModalidadViolenciaAdd, ModalidadViolenciaAjaxList, \
    ModalidadViolenciaEdit, MunicipioAdd, MunicipioAjaxList, MunicipioEdit, NivelEstudioAdd, NivelEstudioAjaxList, \
    NivelEstudioEdit, NivelViolenciaAdd, NivelViolenciaAjaxList, NivelViolenciaEdit, OcupacionAdd, OcupacionAjaxList, \
    OcupacionEdit, ReligionAdd, ReligionAjaxList, ReligionEdit, TipoCasoAdd, TipoCasoAjaxList, TipoCasoEdit, \
    TipoViolenciaAdd, TipoViolenciaAjaxList, TipoViolenciaEdit, ViolentometroAdd, ViolentometroAjaxList, \
    ViolentometroEdit, ViveConAdd, ViveConAjaxList, ViveConEdit, AsesorCallcenterAdd, AsesorCallcenterAjaxList, \
    AsesorCallcenterEdit, PsicologoAdd, PsicologoAjaxList, PsicologoEdit, ReporteroAdd, ReporteroAjaxList, \
    ReporteroEdit, ContactoInstitucionAdd, ContactoInstitucionAjaxList, ContactoInstitucionEdit
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.login, name='login'),

]
