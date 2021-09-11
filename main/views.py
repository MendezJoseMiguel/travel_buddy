from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from django.http import HttpResponseRedirect
from .models import Viajes, User


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

        return render(request, 'addtrip.html')

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
    context = {

        'ver_viaje': ver_viaje
    }
    return render(request, 'verviaje.html', context)

@login_required
def destroytrip(request,id):

    destroy_trip = Viajes.objects.get(id=id)
    destroy_trip.delete()
    
    return redirect("/travels")

@login_required
def canceltrip(request,id):
    
    pass
    
@login_required
def join_travel(request,id):
    pass