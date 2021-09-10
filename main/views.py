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

    context = {
        'viajes': viajes
    }
    return render(request, 'index.html', context)

