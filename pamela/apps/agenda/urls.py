from django.urls import path, include
from .views import *
urlpatterns = [
    path('getTurn/', get_turn, name= "getTurn"),
    path('turnCreate', turnCreate, name= "turnCreate"),
    #path('allTurn/', all_turns, name= "allTurn"),
    path('turnos/', turnos_disponibles, name= "turns"),
    path('perfil/', perfil, name= "perfil"),
    path('typeSession/', TypeSessionCreate.as_view(), name= "typeSession"),
    path('cuentas/', AcountListView.as_view(), name= "cuentas"),
]
