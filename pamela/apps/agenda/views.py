from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy

from datetime import datetime, timedelta, time

from django.views.generic import CreateView, ListView

from my_functions import *

from apps.login.forms import AcountForm
from .forms import *

# My models
from .models import *
from apps.login.models import *



# Create your views here.


def get_turn(request): # confirmacion para recervar el turno
    if not valid_acount(request):
        return redirect('/login')
    content = {}
    if request.method == "POST":
        content["button_text"] = "Aceptar"
        data = request.POST.copy()

        if data:            
            #convertirmos el turno a tipo turn
            new_turn = data["turn"].split()

            new_turn = Turn.create_from_strings(date=new_turn[1], time=new_turn[4], user_id=request.user.id)

            if isinstance(new_turn, Turn):
                
                new_turn.get_turn()

                content["turn"] =  new_turn
                content["day_week"] = new_turn.day_of_week()                
                content["day"] = new_turn.get_day()
                content["month"] = new_turn.month_in_spanish()
                content["time"] = new_turn.formatted_time()
                content["msj"] = "Quiere tomar el turno?"
                return render(request, 'agenda/get_turn.html', content)
                
            else:
                return HttpResponse(f'===== Error no es instacia {new_turn} =====')
        else:
            return HttpResponse("===== Error empty data =====")
    elif request.method == "GET":
        content["button_text"] = "Tomar turno"
    return render(request, 'agenda/get_turn.html', content)

def turnCreate(reuqest): # crea el turno y lo guarda en la base de datos

    if reuqest.method == "POST":
        data = reuqest.POST

        if data:
            turn_str = data["turn"].split()
            fecha = turn_str[1]
            hour = turn_str[3]

            if not Turn.objects.get(date=fecha,time=hour).DoesNotExist:
                new_turn = Turn.create_from_strings(user_id=reuqest.user, date=fecha, time=hour)
                new_turn.save()
            
            return redirect(reverse_lazy("turns"))
    return redirect(reverse_lazy("getTurn"))


'''def all_turns(request):
    if not valid_acount(request):
        return redirect('/login')

    return HttpResponse(f"{list(Turn.objects.all())}")'''


def turnos_disponibles(request): # genera una lista de turnos disponibles teniendo en cuenta los q estan reservados
    if not valid_acount(request):
        return redirect('/login')
    
    context = {"button_text": "Buscar"}
    context["title"] = "Turnos disponibles"
    context['boton_name'] = "Buscar"


    search_form = SearchForm(request.GET)  # Crea una instancia de SearchForm con los datos de la solicitud
    if search_form.is_valid():
        
        context["search_form"] = search_form

        if search_form.cleaned_data['day_of_week']:
            day_search = [search_form.cleaned_data['day_of_week']]
        else:
            day_search = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

        if search_form.cleaned_data['date']:
            fecha_init = search_form.cleaned_data['date']
            fecha_init = datetime.combine(fecha_init, datetime.min.time())
        else:
            fecha_init = datetime.now()
        
        if not (search_form.cleaned_data['date'] and search_form.cleaned_data['day_of_week']):
            search_form = SearchForm()
            context["search_form"] = search_form

    else:
        search_form = SearchForm()
        context["search_form"] = search_form
        fecha_init = datetime.now()
        day_search = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

    # guardamos el valo para hacer la busqueda
    #
    fecha_init = fecha_init.replace(hour=0, minute=0, second=0, microsecond=0)
    fecha_init = datetime.combine(fecha_init, datetime.min.time())
    
    fecha_search = fecha_init
    
    
    # Calcular la fecha final (3 meses desde la fecha actual)
    fecha_fin = fecha_init + timedelta(days=90)

    # Generar la lista de horarios disponibles cada 1 hora
    horarios_disponibles = []
    fecha_init += timedelta(hours=9)
    
    
    for i in range(0,89):
        
        for j in range(0,12):
            horarios_disponibles.append(fecha_init)
            fecha_init += timedelta(hours=1)
            
        if fecha_init.hour >= 21:
                fecha_init += timedelta(days=1)
                fecha_init = fecha_init.replace(hour=0, minute=0, second=0, microsecond=0)

        fecha_init += timedelta(hours=9)

    
    #=================================================
    #esto puede ir en una funcion
    #=================================================
    # Obtener los turnos ocupados en el rango de fechas
    turnos_ocupados = Turn.objects.filter(date__range=[horarios_disponibles[0], fecha_fin])

    week_days = []
    horarios_libres = []
    i=0
    for hora in horarios_disponibles:
        fecha = hora  # Obtener la fecha
        temp_turn = Turn(date=fecha)
        day_str = temp_turn.day_of_week()

        if fecha > fecha_search and day_str in day_search: # validacion de la busqueda
            hora_del_dia = hora.time()  # Obtener la hora del día
            

            # Verificar si el turno para esta fecha y hora ya está ocupado
            if not turnos_ocupados.filter(date=fecha, time=hora_del_dia).exists():
                hora_fin = (hora + timedelta(hours=1)).time()

                new_turn = Turn(date=fecha, time=hora_del_dia, time_fin=hora_fin,user_id=request.user)
                horarios_libres.append(new_turn)
                week_days.append(new_turn.day_of_week())
        i +=1

    horarios_libres = zip(horarios_libres, week_days)
    context['turns'] = horarios_libres

    
    return render(request, 'agenda/turnos_disponibles.html', context)


def perfil(request):
    if not valid_acount(request):
        return redirect(reverse_lazy("login"))
    
    context = {
        "title": "Perfil",
        "boton_name": "Actualizar",
    }
    
    if request.method == "GET":
        acount = Acount.objects.get(user=request.user)
        form = AcountForm(instance=acount)  # Inicializa el formulario con la instancia
        context["form"] = form
    elif request.method == "POST":
        acount = Acount.objects.get(user=request.user)
        form = AcountForm(data=request.POST, instance=acount)  # Pasa la instancia para actualizar

        if form.is_valid():
            form.save()  # Guarda los cambios en la base de datos
            return redirect(reverse_lazy("perfil"))  # Redirige a la página del perfil actualizado
    
        context["form"] = form

    
    return render(request, "agenda/perfil.html", context)



class TypeSessionCreate(CreateView): # crea un tipo de sesion
    form_class = TypeSessionForm
    model = TypeSession
    #fields = ['remote', 'in_group', 'social_rounds', 'price']
    success_url = reverse_lazy('typeSession')
    template_name = "agenda/typeSessionForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar datos personalizados al contexto
        context['title'] = 'Typo de turno'
        context['boton_name'] = "Crear"
        return context
    


class AcountListView(ListView):

    model = Acount
    template_name = "agenda/listAcounts.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtener el valor del parámetro de búsqueda desde el formulario
        search_query = self.request.GET.get('name', None)

        if search_query:
            # Filtrar registros por el campo 'nombre' usando icontains
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar datos personalizados al contexto
        context['form'] = AcountSearchForm()
        context['button_text'] = "Buscar"
        return context
    
    def get(self, request, *args, **kwargs):
        # Procesar el formulario de búsqueda
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)
