from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import User


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    
    return redirect("/login")
    

def login(request):
    
    if request.method == "POST":
        print(request.POST['username'])
        print(request.POST['password'])
        user = User.objects.filter(username=request.POST['username'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "name": f"{log_user}",
                    "username": log_user.username,
                    "email": log_user.email,
                    "role": log_user.role
                }

                request.session['user'] = user
                messages.success(request, "Logueado correctamente.")
                return redirect("/")
            else:
                messages.error(request, "Password o Username  incorrectos.")
        else:
            messages.error(request, "Username o password incorrectos.")



        return redirect("/login")
    else:
        return render(request, 'login.html')


def registro(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            
            request.session['register_name'] =  request.POST['name']
            request.session['register_username'] =  request.POST['username']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_name'] = ""
            request.session['register_username'] = ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                name = request.POST['name'],
                username = request.POST['username'],
                email=request.POST['email'],
                password=password_encryp,
                role=request.POST['role']
            )

            messages.success(request, "El usuario fue agregado con exito.")
            

            request.session['user'] = {
                "id" : usuario_nuevo.id,
                "name": f"{usuario_nuevo.name}",
                "username": f"{usuario_nuevo.username}",
                "email": usuario_nuevo.email
            }
            return redirect("/")

        return redirect("/registro")
    else:
        return render(request, 'registro.html')