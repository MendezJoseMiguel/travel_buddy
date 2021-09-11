from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
    path('travels', views.travels),
    path('addtrip', views.addtrip),
    path('view/<id>',views.viewtrip),
    path('viaje/<id>/destroy', views.destroytrip),
    path('canceltrip/<id>', views.canceltrip),
    path('join_travel',views.join_travel)
]
