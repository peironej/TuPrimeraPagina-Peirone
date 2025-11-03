from django.contrib import admin
from .models import Marca, Categoria, EspecificacionesTecnicas, Monitor

admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(EspecificacionesTecnicas)
admin.site.register(Monitor)