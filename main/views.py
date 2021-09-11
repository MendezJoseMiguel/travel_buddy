from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from django.http import HttpResponseRedirect
from .models import Viajes, User
from datetime import date


@login_required
def index(request):
    
    return redirect('/travels')

@login_required
def travels(request):

    viajes = Viajes.objects.all()
    no_id_traveller = request.session['user']['id']
    viajeros_full = Viajes.objects.all()
    viajeros_yes = viajeros_full.exclude(travellers = no_id_traveller )
    viajes_propios = viajeros_full.filter(travellers = no_id_traveller)

    context = {
        'viajes_propios': viajes_propios,
        'viajeros_yes': viajeros_yes
    }
    return render(request, 'index.html', context)

@login_required
def addtrip(request):

    if request.method == "GET":
        fecha_actual= date.today().strftime('%Y-%m-%d')

        context = {

            "fecha_actual": fecha_actual

        }

        return render(request, 'addtrip.html')

    if request.method =='POST':

        errors = Viajes.objects.validador_basico(request.POST)

        if len(errors) > 0:

            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/addtrip')

        else:

        

            viaje_nuevo = Viajes.objects.create(
                        destino = request.POST['destino'],
                        fecha_partida = request.POST['fecha_partida'],
                        fecha_salida=request.POST['fecha_salida'],
                        plan = request.POST['plan'],
                        creater_id=request.session['user']['id']
                    )

    return redirect("/travels")

@login_required
def viewtrip(request,id):

    ver_viaje = Viajes.objects.filter(id=id)[0]
    creador = ver_viaje.creater.id
    viajeros = ver_viaje.travellers.exclude(id = creador)
    context = {

        'ver_viaje': ver_viaje,
        'viajeros' : viajeros
    }
    return render(request, 'verviaje.html', context)

@login_required
def destroytrip(request,id):

    destroy_trip = Viajes.objects.get(id=id)
    traveller = request.session['user']['id']
    if traveller == destroy_trip.creater.id:

        destroy_trip.delete()
        messages.warning(request, "¡Has Eliminado el viaje seleccionado!")

    else:
        messages.error(request, "¡Solo puedes los Viajes que has Creado!")
    
    return redirect("/travels")

@login_required
def canceltrip(request,id):
    trip_cancel = Viajes.objects.get(id=id)
    traveller = request.session['user']['id']
    trip_cancel.travellers.remove(traveller)
    messages.warning(request, "Ups!, ¡parece que ya no quieres viajar!")
    
    return redirect("/")
    
@login_required
def join_travel(request,id):
    
    trip_join = Viajes.objects.get(id=id)
    traveller = request.session['user']['id']
    trip_join.travellers.add(traveller)
    messages.success(request,"Yeah!, ¡Vamos de Viaje!")
    return redirect("/")