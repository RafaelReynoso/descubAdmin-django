from django.urls import path
from .views import *
from .import views

urlpatterns=[
    ######################## ------USUARIO------ ########################
    path('usuarios/',UsuarioView.as_view(), name= 'usuario_list'),
    path('usuarios/<int:id>',UsuarioView.as_view(), name= 'usuario_process'),
    path('usuarioListado/',views.usuarioListado, name='usuarios'),


    ######################## ------MURALISTA------ ########################
    path('muralistas/',MuralistaView.as_view(), name= 'muralista_list'),
    path('muralistas/<int:id>',MuralistaView.as_view(), name= 'muralista_process'),

    ######################## ------MURAL------ ########################
    path('murales/',MuralView.as_view(), name= 'mural_list'),
    path('murales/<int:id>',MuralView.as_view(), name= 'mural_process'),

    ######################## ------COLOR------ ########################
    path('colores/',ColorView.as_view(), name= 'color_list'),
    path('colores/<int:id>',ColorView.as_view(), name= 'color_process'),

    ######################## ------PALETA------ ########################
    path('paletas/',PaletaView.as_view(), name= 'paleta_list'),
    path('paletas/<int:id>',PaletaView.as_view(), name= 'paleta_process'),

    ######################## ------SCAN------ ########################
    path('scans/',ScanView.as_view(), name= 'scan_list'),
    path('scans/<int:id>',ScanView.as_view(), name= 'scan_process'),

]